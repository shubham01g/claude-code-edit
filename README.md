# EDIT: Claude edits my Instagram reels

You commented "EDIT," so here's the setup.

I don't edit my reels anymore. I record one horizontal video with all my scripts in it, and Claude Code turns it into finished vertical reels.

This pack is the exact skill I use, plus the **style bible** Claude wrote after studying four viral reels frame by frame.

## What it does

1. **Splits** one long recording into one clip per script. I say "Script 1", "Script 2"… out loud while recording.
2. **Cuts** each clip down to the last clean take of every line. Restarts, mistakes and dead air are removed, and every cut is checked against the real audio.
3. **Edits** each reel in the reference style:
   - the layout switches every 1–3 seconds (split screen, full graphic, full face)
   - captions are 1–3 words at a time, so you can read them on any phone
   - real screenshots and code shots appear when you mention them
   - soft tap sounds on scene changes
   - audio is set to -14 LUFS, the loudness Instagram expects
4. **Builds a review page** so you can watch every reel before posting.

## The style rules it learned

These came from pulling 2 frames per second out of 4 viral reels in my niche:

- The screen changes about every **1.5 seconds**.
- The face is hidden about **half the time**.
- Captions are only **1–3 words**.

The full breakdown is in [`style-bible.md`](Instagram/reference-analysis/style-bible.md). Swap in your own reference reels and Claude can rewrite it for your niche.

## What you need

- Claude Code
- Windows. My setup is Windows-first; Mac and Linux work with small path changes, and Claude can make them for you.
- Python and ffmpeg. The setup script installs both, plus [video-use](https://github.com/browser-use/video-use) for cuts and local Whisper transcription.
- Node.js and the Remotion project in `YouTube/remotion/` for the graphics.

## Files in this pack

| File | What it is |
|---|---|
| [`.claude/skills/insta-reel/SKILL.md`](.claude/skills/insta-reel/SKILL.md) | The skill: the batch workflow + every lesson learned on real footage |
| [`.claude/skills/video-edit/`](.claude/skills/video-edit/) | The pipeline scripts (split, cut, plan, render) |
| [`Instagram/reference-analysis/style-bible.md`](Instagram/reference-analysis/style-bible.md) | The style rules |
| [`YouTube/remotion/`](YouTube/remotion/) | The React components that draw the graphics and captions |

## Setup

1. Download this repo (green **Code** button → **Download ZIP**) and copy everything in this repo except README.md and LICENSE into your project folder.
2. Run the setup once:
   ```
   powershell -ExecutionPolicy Bypass -File .claude/skills/video-edit/scripts/setup.ps1
   ```
3. Install the Remotion project:
   ```
   cd YouTube/remotion && npm install
   ```
4. Restart Claude Code.

Easier: open Claude Code in your project and say *"Set up the insta-reel skill from this repo and tell me if anything is missing."*

## How to use it

1. Record all your scripts in one take. Before each one, say "Script 1", "Script 2" and so on. Restarting a line is fine, because the cut keeps your last clean take.
2. Put the file in `Instagram/batches/<date>/raw/`.
3. In Claude Code:
   ```
   /insta-reel batch <date>
   ```
4. Watch the review page, tell Claude what to fix, and post from the `final/` folder.

## Tips from my first batch

- **Keep the native frame rate.** Converting 30 fps to 24 fps and speeding up the clip made my first renders look glitchy.
- **Render one reel at a time.** Parallel renders on a nearly full disk failed.
- **Look at the camera lens, not the screen.** If your webcam sits under your monitor, read from a narrow strip right above it.

---

Made by [@shubham_gunjal_ai](https://instagram.com/shubham_gunjal_ai). My reels are edited exactly this way.
