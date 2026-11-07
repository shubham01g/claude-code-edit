---
name: insta-reel
description: Use when turning horizontal talking-head recordings into vertical Instagram Reels / YouTube Shorts — a whole batch session ("Script 1… Script 15") or a single take. Splits the session per script, cuts each to the last clean take of every line, then edits it in the reference-reel style (split / full-graphic / full-face layouts switching every 1–3 s, styled captions, real screenshots, soft taps, -14 LUFS). Trigger on 'edit the reels', 'edit this reel', 'make a reel', 'insta reel', 'vertical video', 'edit this short', 'I recorded the batch', or when the user drops a short clip meant for Instagram.
argument-hint: batch <YYYY-MM-DD>  |  <slug>  |  <path-to-recording>
---

# Insta Reel — horizontal recording → finished 9:16 reels

**Read first, every run:** `Instagram/reference-analysis/style-bible.md` (what the reference reels do,
frame by frame) and **Learned Lessons** at the bottom of this file.

Run every command with the venv interpreter and UTF-8 output:
`PYTHONUTF8=1 YouTube/video-use/.venv/Scripts/python.exe .claude/skills/video-edit/scripts/run_pipeline.py <cmd> <dir>`

## Auto-Improvement Protocol
When the user points out something wrong with a reel: fix it, add the lesson to **Learned Lessons**,
re-render. Style changes that apply to every reel go in the style bible too.

## The weekly loop (what the user runs)
`/insta-radar` → new scripts + teleprompter (Lens mode) → he records ONE file → `/insta-reel batch <date>` →
review page + `final/` folder → he posts → next batch. Everything below is the second half.

## Layout
```
Instagram/batches/<date>/            one recording session
  scripts.json  batch-page.html      from /insta-radar
  raw/<session>.mp4                  the whole session ("Script 1" … "Script N")
  tracker.json                       status per reel: raw → cut → rendered → approved → posted
  plans.py                           writes every reel's edit/plan.json (scene plan, phrase-anchored)
  review-notes.json                  {slug: "what the cut changed / what to check"} for the review page
  final/NN-<slug>.mp4                hard links to every finished reel — what he watches and posts
  review.html                        the review page (published as an Artifact)
Instagram/reels/<slug>/              one reel
  raw/<slug>.mp4   script.json       written by `batch`
  edit/edl.json final.mp4 timeline.md timeline_words.json caption_fixes.auto.json
  edit/cut_fixes.json                hand fixes to the cut that survive autocut re-runs (optional)
  edit/plan.json → reel.json → reel.mp4   edit/verify/sheet.jpg (one frame per scene)
YouTube/assets/ig/                   screenshots for graphics (src "ig/<name>.png")
Instagram/music/                     music beds (only tracks he supplied) + sfx/tap.wav (auto-made)
```

## Batch workflow (the normal case)
`$PY` = `PYTHONUTF8=1 YouTube/video-use/.venv/Scripts/python.exe`, `$S` = `.claude/skills/video-edit/scripts`.
**Render one reel at a time** (lesson 15). Check C: has a few GB free before rendering.

1. **Split** — `$PY $S/run_pipeline.py batch Instagram/batches/<date>` (small.en, ~3.5 min for 15 min of
   footage). Finds each spoken "Script N" (the last slate wins), cuts each span into `Instagram/reels/<slug>/raw/`,
   prints coverage per script. Under ~80% → read that span's transcript. A span with only one line = a false
   start: mark it `"not recorded"` in tracker.json and delete its reel folder.
2. **Cut all** — `$PY $S/reel_batch.py cut Instagram/batches/<date>` (ingest medium.en → autocut → cut_fixes →
   render cut at the camera's fps → timeline). Read its report, reel by reel:
   - every `restart cut` line must be a real flub; `MISSING` → find the line in the transcript (paraphrase?);
   - read each `edit/timeline.md` end to end: doubled words, a stray fragment ("and and", "sender and it…"),
     an unfinished list ("…and what") → add `{"remove": [a, b]}` (raw-clip seconds, from silencedetect
     -50 dB, never from Whisper word times) to `edit/cut_fixes.json` and re-run `cut --only <slug>`.
3. **Assets** — per script, list the visuals it names. Real pages: `$PY $S/webshot.py YouTube/assets/ig/x.png
   <url> --crop …`; his own files (skills, code, reports): `$PY $S/codeshot.py YouTube/assets/ig/x.png <file>
   <start> <end> --title … --hi …`; data (radar table, stats) → render a small HTML from the real JSON and
   webshot it. Look at every shot (cookie banners, blank animated heroes, cropped text).
4. **Plan** — write `Instagram/batches/<date>/plans.py` (copy the previous batch's as the template: BASE
   settings + `P[slug] = dict(captions, captionFixes, scenes=[S(on, layout, theme, component, props, end=…)])`).
   Anchors are words he SAID (timeline.md), not the script. Per script: `captions.style` = scripts.json
   `captionStyle`, keyword in `keywords`; hook = `ReelHeadline` with scripts.json `headline`; every proof line
   gets a real visual; stats count from scene start (`countAt: 0.1`); lists show their first item at 0.1.
   Don't plan face gaps or pacing — `reel_plan.py` does that (lesson 14/17).
5. **Edit all** — `$PY $S/reel_batch.py edit Instagram/batches/<date>` → plans.py → reel_plan → render (3 tries)
   → `final/NN-slug.mp4` → frame sheet + loudness → tracker → `review.html`. A `PLAN FAILED: phrase not found`
   prints the transcript around it: fix the anchor in plans.py, re-run `edit --only <slug>`.
6. **Look** at every `edit/verify/sheet.jpg` (Read it): a stat showing 0, an empty list, a scene with nothing in
   it, a caption misspelling a tool name (add `captionFixes`, phrases allowed: `"Anti -Gravity": "Antigravity"`),
   a headline repeated. Fix in plans.py → `edit --only …`.
7. **Hand over** — write `review-notes.json` (one line per reel: what the cut changed), re-run
   `$PY .claude/skills/insta-reel/build_review.py Instagram/batches/<date>`, publish `review.html` as an Artifact,
   give him the link + the `final/` folder path. Fixes after his review: plans.py / cut_fixes.json + `--only`.

Single take (not a batch): put it in `Instagram/reels/<slug>/raw/`, `ingest`, then cut with the
silence-trim rules in Learned Lesson 4 (no script → no autocut), then continue from `render`.

## reel.json v2

```json
{
  "version": 2,
  "face":     { "x": 0.47, "y": 0, "scale": 1.0 },
  "faceFull": { "x": 0.47, "y": 0, "scale": 1.05 },
  "speed": 1.08,
  "music": { "src": "lofi-01.mp3", "volume": 0.12 },
  "scenes": [
    { "at": 0.0, "duration": 2.4, "layout": "split", "theme": "cream", "component": "ReelHeadline",
      "props": { "text": "I spy on my competitors' {Instagram}", "image": "radar-page.png" } },
    { "at": 2.4, "duration": 2.1, "layout": "full", "theme": "dark", "component": "ReelTerminal", "props": { … } },
    { "at": 6.1, "duration": 2.0, "layout": "split", "theme": "glass", "component": "ReelPills", "props": { … } }
  ],
  "captions": { "style": "bold", "keywords": ["36x"], "accent": ["median"] }
}
```

| Field | Default | Meaning |
|---|---|---|
| `version` | 1 | `2` turns on everything below. v1 files (e.g. `mvp-14-days`) still render as before |
| `layout` (scene) | split | `split` graphic top / medium face · `full` graphic only · `face` punch-in. **Gaps between scenes = face** |
| `theme` (scene) | glass | `cream` (brand) · `dark` · `glass` (blurred footage). Vary it scene to scene |
| `split` | 0.43 | graphics share of the height in split |
| `face` / `faceFull` | see above | crops for split / face. Put `x` on his nose. `faceFull.scale` > 1.1 on 1080p looks soft |
| `speed` | 1.0 | Keep 1.0: any speed-up drops frames and the face judders (lesson 17). Applied at the end; reel.json times stay on final.mp4 |
| `faceMode` | — | `"cta"`: full-face close-up only for the closing CTA, every other face gap holds the previous graphic in split (used while his eyes are off-lens, lesson 18). Omit once he records in Lens mode with good eye contact |
| `maxScene` / `faceShare` | 3.6 / 0.15 | plan-only pacing knobs for `reel_plan.py` |
| `music` | none | file in `Instagram/music/` or `assets/`, normalised, `volume` 0.08–0.15, 2 s fade. Ask the user for tracks; never use a track he hasn't supplied |
| `sfx` | on (v2) | soft tap on each graphic's entrance. `false` to mute, `{ "volume": 0.35 }` |
| `captions.style` | bold | `bold` caps in a dark box · `clean` sentence case, keywords italic serif · `editorial` serif italic caps. **Use the script's `captionStyle`** |
| `captions.keywords` | script keyword | words in brand orange (numbers, the tool name, the CTA word) |
| `captions.accent` | — | 1 word every ~5 s in Caveat on its own line ("differently", "free") |
| `captionFixes` | auto | on top of `caption_fixes.auto.json` |

Voice is always normalised to −14 LUFS in v2.

### Planning the scenes (the style bible, applied)
- **Switch every 1–3 s.** Target shares: split ~38%, full ~45%, face ~15–20% (`reel` prints the actual mix).
- **Hook (0–2.5 s):** `ReelHeadline` in split with the script's `headline` text (`{phrase}` = orange box) and,
  if there is one, a real screenshot under it. First switch by 2.5 s.
- **The CTA always ends on face** (leave it as the last gap), keyword in `captions.keywords`. Other face moments come from
  pacing (`faceShare`) — or none with `faceMode: "cta"`.
- **Every proof line gets a real visual** landing on its word (scene-relative time = word start − scene `at`):
  screenshot > screen recording > terminal/chat mockup > abstract graphic. Numbers must be true (`context/about-me.md`).
- Never the same component twice in a row; change `theme` often.

| Component | Props | Use it for |
|---|---|---|
| `ReelHeadline` | `text` (`{hi}`), `at?`, `wordGap?`, `image?`, `imageAt?`, `sub?` | the hook title |
| `ReelScreenshot` | `src`, `tag? {text, tone, at}`, `box? {x,y,w,h,at}` (fractions), `stamp? {at}`, `zoom? {to,at,dur,focus}`, `caption?` | real pages: outline the part he names, BEFORE/AFTER, red X |
| `ReelTerminal` | `title?`, `lines[] {text, at, kind: cmd/out/ok/warn/dim/hi}`, `cps?`, `overline?` | commands, logs, code typing in |
| `ReelChat` | `title?`, `messages[] {from: me/ai, text, at}`, `cps?` | prompting Claude |
| `ReelAppCard` | `overline?` ("The first"), `icon?` (emoji) or `image?`, `name`, `nameAt?`, `sub?` | numbered tool / skill beats |
| `ReelPills` | `overline?`, `items[] {text, at, icon?, tone?}` | lists said one by one |
| `ReelSteps` | `overline?`, `steps[] {label, sub?, icon?, at}` | pipelines (scrape → verify → write → send) |
| `ReelMedia` | `src` (video/image), `startFrom?`, `fit?`, `bleed?`, `label?` | full-bleed B-roll / screen recording (layout `full`) |
| `ReelStat` | `value`, `label`, `overline?`, `countAt?`, `countFor?`, `labelAt?`, `chip?` | one hero number counting up |
| `ReelBars` / `ReelChecklist` / `ReelFlatline` / `ReelTitle` / `ReelComment` / `ReelImages` | (v1) | still available |

Panel sizes: split ≈ 950×590, full ≈ 950×1240 (components scale up 1.25× in full). New component →
`YouTube/remotion/src/reel/scenes2.tsx`, register it in `REEL_SCENES_V2` and in `SCENES` in `reel.py`.

### Assets
~45% of a reference reel is screenshots of the real thing. Per script, list the shots it needs.
Capture web pages yourself (Chrome tools → `assets/`), use the user's existing files (skills, pages,
artifacts), and ask him only for screen recordings of his own tools. Never draw a fake screenshot of a
real product.

## Checks before handing over
`--still` inside every scene and in every face gap, and **look**: face framed (whole head, eyes ~25–30%
from top), captions spelled like the script, nothing under the top 150 px, no caption over a face's mouth,
text never cut off. After the render: contact sheet end to end, duration ≤ 45 s, `ebur128` ≈ −14 LUFS.

## Learned Lessons
1. **Layout comes from his reference reels (2026-10-11, v1):** face bottom, graphics top, captions on the seam.
   Superseded for new reels by lesson 5, kept for v1 files.
2. **Reels keep the camera's frame rate (30 fps)** — superseded 2026-11-06: 30 → 24 fps dropped 1 frame in 5 and
   the user saw the motion stutter. `run_pipeline.py render` sets `VIDEO_USE_FPS` from the source for any project
   under `Instagram/` (one-line patch in video-use `helpers/render.py`, logged). Long-form YouTube stays 24 fps.
3. **Glass, not white** (v1). In v2, cream is allowed — it's the brand palette and one reference uses it.
4. **Single-take silence trim:** silencedetect `-32dB:d=0.25` for real speech edges; cut pauses ≥ 0.5 s;
   pad 60 ms head / 100 ms tail.
5. **(2026-11-06) v2 style from 4 reference reels, frame by frame** (style bible): three layouts rotating
   every 1–3 s, face hidden ~40% of the time, captions 1–3 words with coloured keywords, real screenshots,
   a continuous bed under the voice, ending on full face with the comment keyword.
6. **(2026-11-06) 1080p source:** the full-face punch-in is already a 1.78× upscale. Keep `faceFull.scale`
   ≤ 1.1, `y` 0 — scale 1.2 cut off his hair and centred his chin.
7. **(2026-11-06) Autocut tail pads** can swallow a Whisper phantom word ("And") after the CTA; pads now stop
   at the next word and caption words under 60 ms are dropped.
8. **(2026-11-06, first real batch) Never trust Whisper word edges.** It stretched a first word back over a
   2 s pause (dead head on reel 1) and gave "Comment" zero length 0.3 s late (CTA clipped). Autocut now
   checks the real audio (silencedetect −50 dB; his room is gated ≈ −85, speech ≈ −37 RMS): edges snap
   to where speech starts/stops and pauses > 0.4 s inside a line are cut.
9. **(2026-11-06) Take matching:** on equal recall the tightest span wins (a stray earlier "it" dragged a
   line over the previous line's retake); long lines (10+ words) match at 50% (he paraphrases lists);
   takes grow ≤ 4 words in the same breath (a misheard last word was being chopped off the audio).
10. **(2026-11-06) Restarts inside a take** are cut automatically: a word trailing off ("how to…") then the
   restart, or 2+ words said again within 8 words. Not a restart when the script repeats the phrase
   itself ("my own experience and my own proof"), or a 2-word repeat across a comma/sentence end
   (lists: "what we decided, what we shipped"). Read the `restart cut` lines — each one must be a real flub.
11. **(2026-11-06) Auto caption fixes** only map sound-alikes (same first letter, similar length), never
   common words ("the" → "that" was him paraphrasing) and never digits (they read better on screen).
12. **(2026-11-06) Captions follow what he said, not the script,** when he paraphrased — override an auto fix
   with `captionFixes: {"comes": "comes"}`.
14. **(2026-11-06) Pacing is automatic** (`reel_plan.py`): scenes > 3.6 s split at word starts into pieces
   that alternate split/full (the graphic keeps its state), and only *quiet* pieces (nothing new appears)
   become face punch-ins, up to ~15% face. Headlines are never split: max 3 s, then face. Plan the
   graphics; let the planner do the cadence. A stat should count from its scene start (`countAt: 0.1`) —
   a "0" sitting on screen before the number is said looks broken; same for a list that opens empty.
15. **(2026-11-06) Render one reel at a time.** Two parallel Remotion renders on the same machine failed
   with "No frame found at position …" (also with C: nearly full); sequential renders took ~65 s each and
   never failed. Check with `reel_sheet.py <reel> --video` (frames from reel.mp4, seconds not minutes).
16. **(2026-11-06) Batch scene plans live in the batch folder** (`Instagram/batches/<date>/plans.py` writes
   every reel's `plan.json`); manual EDL fixes are noted in `edl.json` → `manual` — re-apply after any
   `autocut` re-run. The review page is `build_review.py` → `review.html` → Artifact.
17. **(2026-11-06, his review) "Glitchy after the first 10 s"** = two things: frame dropping (24 fps + 1.1× speed)
   and micro jump cuts (every pause > 0.4 s was cut, mid-sentence). Now: native 30 fps, speed 1.0, inside a line only
   pauses > 0.7 s are cut (`INLINE_GAP`), and `reel_plan.py` snaps every scene start / layout switch onto a cut
   point so each jump cut is hidden by a graphic change. Check: every cut in edl.json lands on a scene boundary.
18. **(2026-11-06, his review) Eye contact:** he reads off-lens and viewers notice. Teleprompter text must sit
   right under the lens (narrow column, big font, read from ~1 m) or use gaze correction — see decisions log.
13. **(2026-11-06) Landscape screenshots in `full` look small** — crop them close to portrait (≈ 1250×830) or
   point a `box` at the part he names. Real-file screenshots (skills, code, reports) are rendered with
   `codeshot.py OUT.png FILE START END --title … --hi 3,4` (dark editor, line numbers) into `YouTube/assets/ig/`.
