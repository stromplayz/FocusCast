# 🎙️ Focus Cast — the audio library of FocusLinks Listen

> **FocusLinks Listen** · `listen.focuslinks.in` — *Listen. Learn. See better.*
> The show: **Focus Cast by focuslinks**. An automated optometry audio-library factory:
> plain-text scripts in, finished episodes out — rendered on Kaggle's free GPU,
> organized, catalogued, and committed back to this repo by GitHub Actions. Hands-off.

![series](https://img.shields.io/badge/series-01_Optometry_Foundations-8A2BE2)
![episodes](https://img.shields.io/badge/episodes-100_planned_·_20_scripted_(S1%2BS2)-00B4D8)
![engine](https://img.shields.io/badge/engine-Kokoro_82M_·_voicepacks-FF6B6B)
![compute](https://img.shields.io/badge/compute-GitHub_Actions_%E2%86%92_Kaggle_T4-181717)
![license](https://img.shields.io/badge/license-proprietary_·_all_rights_reserved-red)

---

## 🏭 How the automation works (the whole loop, zero clicks after launch)

```
 library/series/…/S01E01-….txt          # scripts carry their own metadata + engine tag
        │
        ▼  Actions: Render Episodes (Kaggle GPU)
 [1] estimate  ──► calibrated ETA printed to the run summary
 [2] push      ──► one Kaggle GPU kernel (Tesla T4) receives every episode
 [3] render    ──► per-script tags choose engine (kokoro) + voices (presets)
                   single narrator or dual narrator (Host + Guide)
 [4] pull      ──► audio lands in the library hierarchy
                   rendered/series-01-optometry-foundations/season-NN-…/ep-NN-…/
        │
        ▼
 [5] catalog   ──► library/master.json auto-updated (raw mp3 URLs + durations + all metadata)
 [6] commit    ──► rendered/ + master.json committed · artifact uploaded · timing report posted
```

Run it: **Actions → Focus Cast · Render Episodes (Kaggle GPU) → Run workflow** →
leave the default (full **Season 1 + Season 2, all 20 episodes**) or edit the list → **Run**.
Typical wall time for a 20-episode batch: **~45–60 min** (Kokoro ≈ 25–30× realtime + queue).
One season only? Pass just that season's ten paths in the `episodes` input.

Requires repo secrets `KAGGLE_USERNAME` / `KAGGLE_KEY` (configured ✓) on a
**phone-verified** Kaggle account (GPU gate — unverified accounts silently get CPU-only kernels).

---

## 📜 The library folder — where episodes live

```
library/
├── series/series-01-optometry-foundations/
│   ├── series.json                       # 🔒 LOCKED Series-01 manifest (100 eps, 10 seasons,
│   │                                     #    core idea, anti-repetition master rule)
│   ├── season-01/                        # 🌱 "Understanding Optometry" · S01E01–E10
│   │   ├── S01E01-what-is-optometry.txt
│   │   ├── …
│   │   └── S01E10-your-journey-through-optometry.txt
│   └── season-02/                        # 👁 "The Eye as a Visual Organ" · S02E01–E10
│       ├── S02E01-why-do-we-have-eyes.txt
│       ├── …
│       └── S02E10-following-the-path-of-vision.txt
├── presets/voices.json                   # 🎭 premade character→voice presets (voicepacks)
└── master.json                           # 📇 auto-updated library catalogue
```

**One series, many seasons.** Season 1 and Season 2 are both Series 1 · *Optometry
Foundations* — the numbering (`S01E05`, `S02E05`) is season-episode, and every rendered
file inherits `series → season → episode` folders from the script header itself.

### Every script carries its own automation instructions (metadata header)

```text
# Title: What Is Optometry?
# Series: Optometry Foundations
# Series No: 1
# Season: Understanding Optometry
# Season No: 1
# Episode No: 1
# Engine: kokoro              ← the model tag: kokoro (default) or voxcpm
# Narration: dual             ← dual narrator (speaker prefixes) or single
# Language: en
# Keywords: what is optometry, optometry definition, …      ← SEO
# Description: What is optometry, really? … Focus Cast by
#              focuslinks …                                ← SEO description
```

The body is dialogue. A speaker tag picks the voice — **no tag = default narrator**:

```text
Host: Welcome to Focus Cast by focuslinks…
Guide: The word is built from two Greek roots…
```

**Brand rule (spoken audio):** scripts always say **"Focus Cast by focuslinks"** — never
"focuslinks dot in". The `.in` domain is written-only branding (README, metadata, site);
TTS would mispronounce it, so the audio never sees it.

That's the whole contract. Drop a new `.txt` in a season folder with a header and it is
renderable — no code changes, ever.

---

## 🎭 Premade presets — consistent voices across the whole library

`library/presets/voices.json` binds **characters** (not scripts) to Kokoro voices, so
Episode 1 and Episode 95 share the same narrator identity:

| Character | Voice (Kokoro-82M) | Style |
|---|---|---|
| **Host** (default) | `af_heart` | warm, curious host |
| **Guide** | `am_michael` | calm optometry teacher — a role, never a named/fictional doctor |
| **Narrator** | `af_nova` | documentary single-narrator episodes |

Why no "Dr. Meera"-style persona? A fictional named clinician misleads listeners about
who is speaking. The **Guide** teaches in the same calm, clinically precise register
without claiming any credential — honest by construction.

Need a new character? Add one line to `voices.json` (choose from ~30 voicepacks listed
inside the file — American/British × male/female), reference the character in a script,
done. **Single-narrator episodes** simply omit speaker tags (or use the `Narrator`
preset). **VoxCPM** (tokenizer-free, zero-shot cloning) stays available for special
immersive episodes via `# Engine: voxcpm`.

---

## 📇 master.json — the library catalogue (auto-maintained)

After every render the workflow runs `scripts/update_master.py`, which rebuilds
`library/master.json` (stale entries whose audio vanished are dropped):

```json
{
  "library": "FocusLinks Listen · Focus Cast",
  "episode_count": 20,
  "episodes": [{
    "id": "S01E01",
    "series_no": 1,
    "series": "Optometry Foundations",
    "season_no": 1,
    "title": "What Is Optometry?",
    "keywords": ["what is optometry", "…"],
    "description": "SEO description…",
    "narration": "dual",
    "engine": "kokoro",
    "voices": { "Host": "af_heart", "Guide": "am_michael" },
    "audio": {
      "mp3": "rendered/series-01-optometry-foundations/season-01-understanding-optometry/…mp3",
      "raw_url": "https://raw.githubusercontent.com/stromplayz/FocusCast/main/rendered/…mp3",
      "duration_min": 28.4
    }
  }]
}
```

Idempotent by design: re-runs update in place, stale entries drop out, anything
without library tags (demos) is ignored. Point any player, app, or website at this
one JSON file and it always knows the whole library.

---

## ⏱ Time estimation (calibrated, not guessed)

The estimator is calibrated against real Kaggle-T4 runs and printed at three moments:
before launch (workflow summary), after completion (estimate vs actual table), and as
`rendered/<slug>.timing.json` committed next to the audio.

| Engine | Model | Throughput (measured) | 30-min episode |
|---|---|---|---|
| **kokoro** (default) | Kokoro-82M, 24 kHz | ~25–30× realtime on T4 | ~2–4 min render |
| **voxcpm** (special) | VoxCPM2, 48 kHz | 20.7 s/chunk on T4 | ~20–25 min render |

Real runs: 5-episode batch ETA 12.0 min → actual 11.4 min; retina (VoxCPM2) ETA 22.4 → actual 26.5 incl. ~4 min queue.

---

## 🗂 Rendered output hierarchy

```
rendered/
├── series-01-optometry-foundations/
│   ├── season-01-understanding-optometry/
│   │   ├── ep-01-what-is-optometry/     S01E01-….mp3 · .meta.json
│   │   └── …
│   └── season-02-the-eye-as-a-visual-organ/
│       ├── ep-01-why-do-we-have-eyes/   S02E01-….mp3 · .meta.json
│       └── …
├── demos/                               # pre-FocusCast engine demos (retina, cochlea)
└── focuscast-batch.timing.json          # latest batch timing report
```

MP3s are committed at 96 kbps mono (spoken-word transparent, repo-friendly);
WAVs stay on Kaggle + in the 30-day Actions artifact (`--no-wav` keeps them out of git).

---

## ✅ CHECKLIST.md — single source of truth for production state

Every episode's lifecycle is tracked in **[CHECKLIST.md](CHECKLIST.md)**:
script ✓ → rendered ✓ → in master.json ✓, per season, plus the quality gates every
script must pass (header fields, speakers, spoken-brand rule, ear-safe writing, length).

---

## 🔒 Series 01 — locked draft & the anti-repetition master rule

**Series 01 · Optometry Foundations** — 100 episodes, 10 seasons — is locked as the
foundation database (full list in `series.json`). **Seasons 1–2 (20 episodes) are now
scripted.** The rule that governs all future series:

> **One concept → one primary teaching home.** Later appearances must add a different
> learning purpose (depth, technique, interpretation, clinical application, or cases) —
> never a re-record. Series 01 E33 *Myopia* → Series 06 *Myopic Refraction: full clinical
> management* → Series 27 *Case: progressive myopia* → Series 28 *Viva: myopia questions*
> are all **different learning purposes**, not duplicates.

Seasons 3–10 stay planned until Seasons 1–2 are rendered and locked.

---

## 💻 Local / CLI use (optional)

```bash
pip install kokoro soundfile numpy espeak-ng ffmpeg   # kokoro path
python scripts/generate_tts.py --episode library/series/…/S01E01-what-is-optometry.txt --outdir /tmp
python scripts/kaggle_render_driver.py --estimate-only --episode library/series/…/S01E01-….txt
python scripts/kaggle_render_driver.py --episode library/…/S01E01-….txt --episode library/…/S01E02-….txt --no-wav
python scripts/update_master.py                       # rebuild the catalogue manually
```

## 📁 Repo layout

```
├── library/                     # 🧠 the Workbench (scripts, presets, catalogue)
├── rendered/                    # 🎧 finished audio in library hierarchy
├── scripts/
│   ├── generate_tts.py          # renderer: headers, dual narration, kokoro/voxcpm, mp3
│   ├── kaggle_render_driver.py  # batch push/poll/pull + ETA + hierarchy mapping
│   └── update_master.py         # master.json builder (idempotent)
├── CHECKLIST.md                 # ✅ production tracker (what exists, what's next)
├── .github/workflows/kaggle.yml # ⚡ the factory (estimate → render → catalogue → commit)
├── .github/workflows/generate.yml  # legacy single-episode CPU renderer
└── .devcontainer/               # Codespaces one-click environment
```

## 🔐 Security & licensing notes

- Kaggle credentials live only in encrypted repo Actions secrets — never in code.
- Phone-verify the Kaggle account or kernels silently lose GPU + internet.
- Rotate any credential that ever appears in chat history.
- **License: FocusLinks Proprietary — all rights reserved.** Nothing in this repo may be
  used, copied, redistributed, or monetized without written permission from FocusLinks.
  Viewing the public repo is the only permitted use.
