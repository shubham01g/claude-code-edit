# Reel Style Bible — learned from 4 reference reels (2026-11-06)

Source reels (in `Example Instagram Reels/`, copies + frames + transcripts in this folder):

| Key | Creator | Length | Words | Pace | Shots (scene cuts) | Avg shot |
|---|---|---|---|---|---|---|
| `mods` | Nate Herk — "Claude code mods are insane. Steal these 3." | 34.5 s | 153 | 272 wpm | 17 | 2.0 s |
| `editvid` | Nate Herk — "Claude has completely changed how I edit videos" | 49.6 s | 229 | 278 wpm | 44 | 1.1 s |
| `dots` | Nick Saraev — "OpenAI Just Dropped Dots" | 35.9 s | 157 | 263 wpm | 12 (+ graphic swaps inside shots) | 3.0 s |
| `popup` | Nate Herk — "This AI Gives Every Shopper a Different Popup" | 66.1 s | 276 | 251 wpm | 43 | 1.5 s |

Method: 2 fps frames + scene-change detection (`cuts.txt`), contact sheets (`<key>/sheets/`),
local whisper transcripts (`<key>/edit/transcripts/ref.json`), ebur128 + silencedetect on audio.
Every rule below cites `reel @ seconds`.

---

## 1. The big pattern: three layouts, rotated every 1–3 s

Every reel cycles between three layouts. Nothing holds longer than ~3 s (`dots` holds longer
shots but swaps the graphic inside them).

| Layout | What's on screen | Share of runtime (approx.) | Examples |
|---|---|---|---|
| **SPLIT** | graphic on top (~43% of height, y 0–830), face below (~57%), caption on the seam | ~38% | mods @0–1.5, @21–24 · popup @0.5–1.5, @20–22 · dots @0–2, @7.5–13.5 |
| **FULL GRAPHIC** | graphic/screenshot/B-roll fills the frame, no face, caption over it | ~45% | mods @2–4, @10–13, @16–20, @24.5–27.5 · editvid @7–9, @26–28 · dots @15.5–24 · popup @13–15.5, @49–51 |
| **FULL FACE** | tight punch-in, face fills the frame, caption on the chest | ~17% | mods @4.5–5, @8–9.5, @31–34 · editvid @2–2.5, @37.5–38.5 · popup @4–4.5, @27.5–28.5, @37–38.5 |

- **The face is hidden almost half the time.** These reels are visual-first: the voice narrates,
  the screen proves. (mods: face visible ~52%, dots: ~50%.)
- **Two face zooms.** The SPLIT face is a medium shot (head + shoulders + room, neon sign visible);
  FULL FACE is a hard punch-in (face fills the width, eyes ~25% from top). Switching between them
  *is* the jump-cut energy — no smooth zooms needed. (popup @3.0 vs @4.0, editvid @1.5 vs @2.0)
- **Nate records horizontal, wide.** editvid @33.5 shows his "RAW FOOTAGE": a 16:9 wide shot of the
  desk. Both face zooms are crops of it. Nick's framed face card (dots) is also a crop of a 16:9 frame.
- **Full face is used for:** the bridge sentence after the hook, emotional/opinion beats
  ("really cheap", "so I never…"), and **always the final CTA** (all 4 reels end on full face).

## 2. Hook (first 0–3 s)

- **Never a plain talking head.** First frame is always a visual + the hook line.
  - mods @0–1.5 / dots @0–2: **headline title** pinned at the top of a SPLIT —
    "People are hacking **[Claude Code]**", "ChatGPT Now Has **[Its Own Computer]**" — black text,
    the key phrase in a solid colour box (orange / blue) in condensed italic serif. Builds word by word.
  - editvid @0–1.5: a **video wall** collage of his past reels + face, with the caption.
  - popup @0–0.5: product logo pixel-reveal, then SPLIT with the product site.
- **First cut by 0.7–2 s** (editvid 0.7, popup 0.7, mods 1.9, dots 2.4).
- **Hook line shape** (transcripts): news/claim in one sentence, no question.
  - "People are now hacking Claude Code itself to stop it from burning through their money"
  - "You can now give ChatGPT a job and just walk away."
  - "This AI makes your website react differently to every person who visits it."
  - "So I taught Claude to edit my videos just by telling it what I didn't like."
- Then **name it** within 5 s: "They're called mods", "It's called Alia", "these things called dots".

## 3. Script structure (all 4 share it)

```
HOOK      0–3 s    one-sentence claim / news / result
NAME IT   3–6 s    "It's called X" / "They're called X, and here's how they work"
PROOF     6–30 s   2–4 concrete items, each = one sentence + one visual
                   ("I've got one called…", "Then there's…", "So now it…")
                   numbers are specific: 500K tokens, ~250 of my last 1,000 prompts, up to 40%
PAYOFF    optional "That's exactly how this video got edited" / "the smartest part is…"
CTA       last 3–5 s  "Just comment EDIT and I'll send it right over to you" /
                      "comment HACKED" / "links in the pinned comment"
```
- 150–160 words for a ~35 s reel; ~230–280 for 50–66 s.
- Pace is **250–280 wpm on screen** — tight cuts with zero gaps (and very likely a slight speed-up).
- First person, "I've built…", "I tossed mine a product launch" — the creator's own use, not a lecture.

## 4. Captions — always on, 1–3 words, on the seam

Two families seen; Nate's newer reels (editvid, popup) are the most consistent and most readable:

**Nate style (adopt this):**
- ALL CAPS, heavy geometric sans (Montserrat ExtraBold–like), white, ~60–70 px on 1080 wide.
- Each chunk sits in a **dark rounded box** (semi-opaque charcoal) — readable on any background
  (editvid's own script @3–7: "white captions on a bright website… now it puts each one on the same dark box").
- 1–3 words per chunk, line-breaks into 2 lines when long ("WHAT I / DIDN'T LIKE" editvid @2.5).
- **Keyword colour:** one word per chunk in a colour — green/teal for positive, red for negative
  (editvid @2 "WHAT I" red, @5 "ON ITS OWN" green, popup @4 "AND INSTEAD" red, @16 "THEN ALIA WATCHES" teal).
- **Script accent word:** one lowercase italic serif word stacked under/over the caps chunk, in the
  accent colour (popup @1.5 "differently", @24 "A-B test", @38.5 "anyways", @65.5 "free trial";
  editvid @14.5 "dynamic", @25.5 "soft").
- **Position:** SPLIT → on the seam (y ≈ 830). FULL FACE → chest (y ≈ 1250–1350).
  FULL GRAPHIC → lower-middle (y ≈ 1350–1450) or the seam line.
- **CTA keyword in quotes + colour:** editvid @48 'JUST COMMENT "EDIT"' (green), mods @32.5 '"Hacked"' (orange).

(mods variant: sentence-case bold sans on light SPLIT, condensed italic serif ALL CAPS on FULL GRAPHIC,
with the previous word ghosted above in serif. Nick: sentence-case medium sans, brand nouns in italic
serif blue. Both readable — but mixing per-layout styles is more work for no clear gain.)

## 5. Graphics vocabulary (what fills the top / the full frame)

Real stuff, not abstract shapes. Ranked by how often they appear:

1. **Real screenshots / screen recordings** — product sites, GitHub, X posts, docs pages
   (editvid @3–5, @9–10, @46; popup @0.5–1.5, @5–6, @11–12; dots @24.5–26.5).
   Enhanced with: **highlight marker** on the spoken words (dots @25–26 "context from ChatGPT memory",
   mods @13 "cache goes cold"), **outline box drawn** around a region in accent colour (mods @21.5, @29, @30.5),
   **red X stamp** over a thing being rejected (popup @30.5–32), **BEFORE / AFTER tag** at top (editvid @3, @9, @20.5).
2. **Code / terminal windows** that type in line by line (mods @6–7.5, editvid @7–8.5, @15.5–17, @31.5–33).
3. **App-icon card** — big rounded icon + name, numbered list beat: "THE FIRST / CACHE KEEPER" (mods @10–11,
   @20–20.5, @26.5–27.5), "Smart Offers" (popup @26–27), "Prism AI" (popup @10–10.5).
4. **Stacking pills / checklist** — rounded white pills appear one per spoken item
   (popup @13–15.5 "Which page… / What their UTM? / Where the traffic came from?", @49–50.5;
   editvid @26–27.5 ✓ wood-tap / muted-click / paper-slide).
5. **Big stat** — number counts up, label under (mods @24.5–26 "~166 → ~250 of my last 1,000 prompts",
   popup @42–44 "+40%", editvid @30–31 "39 → 306 ms" with a line chart).
6. **UI mockups** — dashboards, chat windows, phone with messages typing in (dots @15.5–24, @30.5–34;
   popup @20–22 traffic allocation, @53.5–55 bar chart).
7. **Full-screen B-roll** — stock/AI footage of a person at a laptop (popup @2–3, @32.5–34, @60.5–61.5;
   editvid @17.5–18.5), video wall (editvid @0–1, @39–39.5).

Motion: panels slide/scale in (~0.2–0.3 s), items stagger on the word, text types. Backgrounds vary
per scene: white/cream, dark navy/charcoal, blurred footage, gradient (mods @20 beige, dots @15.5 navy).
**Shubham's brand fits:** mods uses cream + orange accent — the same palette as `YouTube/brand-guidelines.md`.

## 6. Audio

- **A continuous bed under the voice in all 4.** No gap anywhere drops below −50 dB for even 50 ms
  (silencedetect −50 dB / 0.05 s → 0–1 hits per reel). Voice alone with tight cuts would show gaps.
- Integrated loudness: −14 LUFS (mods, editvid), −16 (dots), −20 (popup). LRA 1.6–3.5 LU → heavily compressed voice.
- Soft UI SFX on graphic entrances (editvid's own script @24.8: "soft taps, clicks, and paper sounds" —
  explicitly *not* lasers/zaps).

## 7. Ending

- Full face, CTA caption with the keyword in quotes + colour, held ~1.5–3 s, no outro card
  (mods @31–34, editvid @47.5–49.5, dots @34.5–36, popup @62–66 then a code screen).

---

## What we adopt for Shubham's reels (the spec for `/insta-reel` v2)

| # | Rule | Change vs current `/insta-reel` |
|---|---|---|
| 1 | Three layouts — SPLIT (graphic 43% / face 57%), FULL GRAPHIC, FULL FACE — switch every 1–3 s, face hidden ~40% | Today: SPLIT 50/50 all the time, `full` max twice. **New `layout` per scene.** |
| 2 | Two face zooms: SPLIT = medium crop, FULL FACE = hard punch-in | New `faceFull` crop settings |
| 3 | Hook: headline title (key phrase in an orange box) over a visual for the first 1.5–3 s; first cut by 2 s | New `ReelHeadline` scene |
| 4 | Captions: ALL CAPS heavy sans in a dark box, 1–3 words, one keyword in brand orange (`#F97316`) / green for positives / red for negatives, optional Caveat accent word | Today: 1–2 words sentence case, dark pill. **Restyle + keyword colours + accent word** |
| 5 | Caption position follows layout: seam / chest / lower-middle | New |
| 6 | Graphics: real screenshots + highlight/outline/X/BEFORE-AFTER, terminal typing, app-icon numbered card, stacking pills, stat counter, phone/chat mockup, full-screen B-roll | Add `ReelScreenshot`, `ReelTerminal`, `ReelAppCard`, `ReelPills`, `ReelHeadline`, `ReelBroll`; keep existing 7 |
| 7 | Backgrounds per scene: cream (brand) / charcoal / blurred footage | Today: blurred glass only |
| 8 | Zero-gap cut, ~1.08× speed-up option, voice compressed to −14 LUFS | Tighter cut rules + `speed` in `reel.json` |
| 9 | Quiet music bed under the voice (~−28 LUFS vs −14 voice), 2 s fade out; soft click on scene entrances | New audio pass |
| 10 | End on FULL FACE with `COMMENT "WORD"` in orange, held ≥1.5 s | Today: `ReelComment` graphic. Keep as option, default to the full-face CTA |
| 11 | Scripts: hook → name it → 2–4 proof items → CTA, 120–160 words, first person | Feeds the 15-script batch |

**Assets are the bottleneck.** ~45% of the runtime is screenshots/screen recordings of the real thing.
For every script, Claude lists the shots it needs; Claude captures web screenshots itself (Chrome),
Shubham supplies screen recordings of his own tools, and anything else is built in Remotion.
