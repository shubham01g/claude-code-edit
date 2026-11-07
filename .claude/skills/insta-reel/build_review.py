"""Build <batch>/review.html: one card per rendered reel (frame sheet, length, loudness, caption style, CTA,
the DM to send, what the cut changed). Notes per reel: <batch>/review-notes.json {slug: text} (optional).
usage: build_review.py Instagram/batches/<date>   (video-use venv python)"""
import base64
import html
import io
import json
import re
import subprocess
from pathlib import Path

from PIL import Image

import sys

ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
REELS = ROOT / "Instagram" / "reels"
NOTES = json.loads((BATCH / "review-notes.json").read_text(encoding="utf-8")) if (BATCH / "review-notes.json").exists() else {}


def probe(p: Path) -> tuple[float, float]:
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                             capture_output=True, text=True).stdout.strip() or 0)
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    return d, float(m[-1]) if m else 0.0


def sheet_uri(p: Path) -> str:
    im = Image.open(p).convert("RGB")
    im = im.resize((1080, int(im.height * 1080 / im.width)))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=68, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main() -> None:
    scripts = json.loads((BATCH / "scripts.json").read_text(encoding="utf-8"))["scripts"]
    cards, total_len, done = [], 0.0, 0
    for s in scripts:
        mp4 = REELS / s["slug"] / "edit" / "reel.mp4"
        if not mp4.exists():
            continue
        dur, lufs = probe(mp4)
        total_len += dur
        done += 1
        sheet = REELS / s["slug"] / "edit" / "verify" / "sheet.jpg"
        head = re.sub(r"\{([^}]+)\}", r"<mark>\1</mark>", html.escape(s["headline"]["text"]))
        cta = f'Comment <b>{html.escape(s["keyword"])}</b>' if s.get("keyword") else "Follow"
        send = html.escape(s.get("send") or "nothing to send")
        path = f"Instagram/reels/{s['slug']}/edit/reel.mp4"
        cards.append(f"""
<article class="reel" id="r{s['n']}">
  <header>
    <span class="num">Script {s['n']}</span>
    <h2>{head}</h2>
    <dl>
      <div><dt>Length</dt><dd>{dur:.1f} s</dd></div>
      <div><dt>Loudness</dt><dd>{lufs:.1f} LUFS</dd></div>
      <div><dt>Captions</dt><dd>{html.escape(s['captionStyle'])}</dd></div>
      <div><dt>CTA</dt><dd>{cta}</dd></div>
    </dl>
  </header>
  <p class="note">{html.escape(NOTES.get(s['slug'], ''))}</p>
  <p class="dm"><span>DM when they comment:</span> {send}</p>
  <div class="sheet"><img loading="lazy" src="{sheet_uri(sheet)}" alt="Frames from {html.escape(s['slug'])}, one per scene"></div>
  <p class="path"><code>{path}</code></p>
</article>""")

    missing = [s for s in scripts if not (REELS / s["slug"] / "edit" / "reel.mp4").exists()]
    music_dir = ROOT / "Instagram" / "music"
    music = any(music_dir.glob("*.mp3")) or any(music_dir.glob("*.wav"))
    page = (TEMPLATE.replace("__CARDS__", "\n".join(cards)).replace("__DONE__", str(done))
            .replace("__TOTAL__", str(len(scripts))).replace("__MIN__", f"{total_len / 60:.1f}")
            .replace("__BATCH__", BATCH.name)
            .replace("__DMS__", str(sum(1 for s in scripts if s.get("keyword") and s not in missing)))
            .replace("__MISSING__", "".join(f"<span>Script {s['n']} not recorded</span>" for s in missing))
            .replace("__MUSIC__", "" if music else "<li>No background music yet. Drop 3–5 royalty-free tracks in "
                                                   "<code>Instagram/music/</code> and I'll add a quiet bed.</li>"))
    out = BATCH / "review.html"
    out.write_text(page, encoding="utf-8")
    print(f"review -> {out}  ({done} reels, {out.stat().st_size / 1e6:.1f} MB)")


TEMPLATE = """<title>Reel Batch __BATCH__</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap">
<style>
/* Layout: a single review column of reel cards, each a filmstrip of its scenes, read top to bottom on a phone */
:root {
  --bg: #FDF5EE; --card: #FFFFFF; --fg: #1C1C1E; --muted: #6B6258; --line: #EADFD4;
  --accent: #F97316; --accent-ink: #9A3F06; --mark: #F97316;
  --display: "Poppins", "Segoe UI", system-ui, sans-serif;
  --body: "Inter", "Segoe UI", system-ui, sans-serif;
  --mono: "JetBrains Mono", Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #161210; --card: #211B17; --fg: #F6EEE6; --muted: #B3A698; --line: #3A2F28;
  --accent: #FB923C; --accent-ink: #FDBA74; --mark: #EA6A0E; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #161210; --card: #211B17; --fg: #F6EEE6; --muted: #B3A698; --line: #3A2F28;
  --accent: #FB923C; --accent-ink: #FDBA74; --mark: #EA6A0E; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); }
.wrap { max-width: 1120px; margin: 0 auto; padding-block: 28px 64px;
        padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
        display: grid; gap: 28px; }
.top h1 { font: 800 clamp(26px, 5vw, 40px)/1.1 var(--display); margin: 0 0 8px; text-wrap: balance; letter-spacing: -0.02em; }
.top p { margin: 0; color: var(--muted); max-width: 68ch; }
.facts { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.facts span { border: 1px solid var(--line); border-radius: 999px; padding: 4px 12px; font-size: 13px; background: var(--card); }
.facts b { font-variant-numeric: tabular-nums; }
.todo { border-left: 3px solid var(--accent); padding: 4px 0 4px 16px; display: grid; gap: 4px; }
.todo h2 { font: 600 13px var(--body); letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent-ink); margin: 0 0 4px; }
.todo ol { margin: 0; padding-left: 20px; display: grid; gap: 4px; max-width: 72ch; }
.reel { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 20px; display: grid; gap: 12px; min-width: 0; }
.reel header { display: grid; gap: 6px; }
.num { font: 600 12px var(--body); letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent-ink); }
.reel h2 { font: 800 22px/1.2 var(--display); margin: 0; text-wrap: balance; }
mark { background: var(--mark); color: #FFF; border-radius: 6px; padding: 0 6px; }
dl { display: flex; flex-wrap: wrap; gap: 6px 22px; margin: 4px 0 0; }
dl div { display: flex; gap: 6px; align-items: baseline; }
dt { color: var(--muted); font-size: 13px; }
dd { margin: 0; font-weight: 600; font-variant-numeric: tabular-nums; }
.note { margin: 0; max-width: 80ch; }
.dm { margin: 0; color: var(--muted); font-size: 14px; }
.dm span { color: var(--fg); font-weight: 600; }
.sheet { overflow-x: auto; border-radius: 10px; border: 1px solid var(--line); }
.sheet img { display: block; width: 100%; min-width: 640px; height: auto; }
.path { margin: 0; font-size: 12px; color: var(--muted); overflow-wrap: anywhere; }
code { font-family: var(--mono); }
@media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto; } }
</style>
<div class="wrap">
  <section class="top">
    <h1>__DONE__ reels, edited and ready to review</h1>
    <p>Every reel plays at your camera's own frame rate with no speed-up, and every cut lands on a layout switch, so your face never jumps. Each strip below is one frame per scene, in order.</p>
    <div class="facts"><span><b>__DONE__</b> of __TOTAL__ scripts edited</span><span><b>__MIN__</b> min of reels</span><span>1080×1920</span>__MISSING__</div>
  </section>
  <section class="todo">
    <h2>Before you post</h2>
    <ol>
      <li>Watch them in <code>Instagram/batches/__BATCH__/final/</code>. Tell me the reel number and what to change; fixes are quick re-renders.</li>
      __MUSIC__
      <li>__DMS__ reels promise a DM. Have each thing ready before that reel goes live (listed on each card).</li>
    </ol>
  </section>
__CARDS__
</div>
"""

if __name__ == "__main__":
    main()
