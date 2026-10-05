# FocusLinks Listen · Focus Cast — Production Checklist

> **FocusLinks Listen** · listen.focuslinks.in — *Listen. Learn. See better.*
> Show: **Focus Cast by focuslinks** · Series 1 (Optometry Foundations, 100 eps) · Series 2 (Ocular Anatomy for Optometrists, 100 eps) · Series 3 (Ocular Physiology, 100 eps)
> Track every artifact here. Tick a box only when the thing is real and verified.

---

## 1 · Platform & Branding

- [x] Show name locked: **Focus Cast** (part of the FocusLinks Listen platform)
- [x] Platform name locked: **FocusLinks Listen** — home `listen.focuslinks.in`
- [x] Tagline locked: *Listen. Learn. See better.*
- [x] Spoken brand rule: audio says **"Focus Cast by focuslinks"** — never "focuslinks dot in" (TTS mispronounces the domain; `.in` is written-only branding)
- [x] No named/fictional doctor personas (old "Dr. Meera" removed as misleading) → dual narration is **Host + Guide** (Guide is a role, never named, never claims credentials)
- [x] License switched MIT → **FocusLinks Proprietary License** (all rights reserved, nothing permitted without written permission)
- [x] Domain shortlist documented (final platform home: `listen.focuslinks.in`)

## 2 · Pipeline (workbench)

- [x] Repo: `stromplayz/FocusCast`
- [x] Renderer `scripts/generate_tts.py` — kokoro + voxcpm, header parsing, dual-narrator voice presets
- [x] Driver `scripts/kaggle_render_driver.py` — batch push → T4 render → pull → hierarchy `rendered/series-NN/season-NN/ep-NN/`, calibrated ETA
- [x] Catalog `scripts/update_master.py` — rebuilds `library/master.json` (raw URLs, durations, metadata), drops stale entries
- [x] Workflow `.github/workflows/kaggle.yml` — estimate → render → catalog → commit + timing report
- [x] Presets `library/presets/voices.json` — Host (af_heart), Guide (am_michael), Narrator (af_nova) + ~30 voicepacks
- [x] Series bible `library/series/series-01-optometry-foundations/series.json` — Series 1 locked: 10 seasons × 10 episodes (100 topics), anti-repetition rule
- [x] `library/master.json` reset after test-batch deletion (0 episodes — rebuilds on next render)

## 3 · Quality gates (every script)

- [x] Header has all of: `Title`, `Series`, `Series No`, `Season`, `Season No`, `Episode No`, `Engine`, `Narration`, `Language`, `Keywords`, `Description`
- [x] SEO `Description` (3–5 sentences) + 8–12 `Keywords`
- [x] Speakers are ONLY `Host:` and `Guide:` (or single `Narrator:`) — no named doctors, no credentials claimed
- [x] Brand line said exactly as "Focus Cast by focuslinks" (intro + outro); zero occurrences of `focuslinks.in` / "dot in"
- [x] Written for the ear: no symbols (write "percent", "twenty twenty"), no slashes/ampersands, no URLs
- [x] Target length 4,000–4,500 words ≈ 28–30 min at 150 wpm
- [x] Anti-repetition: one concept → one primary teaching home (checked against series.json)

## 4 · Series 1 · Season 1 — "Understanding Optometry"

| # | Episode | Script | Rendered | In master.json |
|---|---------|--------|----------|----------------|
| 01 | What Is Optometry? | [x] | [ ] | [ ] |
| 02 | What Does an Optometrist Do? | [x] | [ ] | [ ] |
| 03 | The Scope of Optometric Practice | [x] | [ ] | [ ] |
| 04 | Optometry and Eye Care | [x] | [ ] | [ ] |
| 05 | Optometrist, Ophthalmologist and Optician | [x] | [ ] | [ ] |
| 06 | The Optometrist's Role in Patient Care | [x] | [ ] | [ ] |
| 07 | Major Areas of Optometry | [x] | [ ] | [ ] |
| 08 | Clinical and Community Optometry | [x] | [ ] | [ ] |
| 09 | The Modern Optometry Practice | [x] | [ ] | [ ] |
| 10 | Your Journey Through Optometry | [x] | [ ] | [ ] |

Scripts live in `library/series/series-01-optometry-foundations/season-01/` as `S01E01-<slug>.txt` … `S01E10-<slug>.txt`.

## 5 · Series 1 · Season 2 — "The Eye as a Visual Organ"

| # | Episode | Script | Rendered | In master.json |
|---|---------|--------|----------|----------------|
| 01 | Why Do We Have Eyes? | [x] | [ ] | [ ] |
| 02 | From Light to Vision | [x] | [ ] | [ ] |
| 03 | The Eye as an Optical System | [x] | [ ] | [ ] |
| 04 | The Front of the Eye | [x] | [ ] | [ ] |
| 05 | The Back of the Eye | [x] | [ ] | [ ] |
| 06 | The Retina as the Sensory Layer | [x] | [ ] | [ ] |
| 07 | The Optic Nerve and Visual Information | [x] | [ ] | [ ] |
| 08 | The Macula and Central Vision | [x] | [ ] | [ ] |
| 09 | Peripheral Vision | [x] | [ ] | [ ] |
| 10 | Following the Path of Vision | [x] | [ ] | [ ] |

Scripts live in `library/series/series-01-optometry-foundations/season-02/` as `S02E01-<slug>.txt` … `S02E10-<slug>.txt`.

## 5a · Series 1 · Seasons 3–10 — scripted (80 episodes, 100/100 series total)

All eight seasons written by the 8-agent sprint, every script PASS (`scripts/verify_ep.py`), every season E01 opener + E10 finale with next-season tease chain intact.

| Season | Title | Script | Rendered | In master.json |
|--------|-------|--------|----------|----------------|
| 03 | Understanding Vision | [x] 10/10 | [x] | [x] |
| 04 | Optometric Terminology | [x] 10/10 | [x] | [x] |
| 05 | The Optometry Examination | [x] 10/10 | [x] | [x] |
| 06 | Basic Clinical Measurements | [x] 10/10 | [x] | [x] |
| 07 | Understanding Optometric Prescriptions | [x] 10/10 | [x] | [x] |
| 08 | Clinical Communication and Reasoning | [x] 10/10 | [x] | [x] |
| 09 | The Patient Journey | [x] 10/10 | [x] | [x] |
| 10 | Foundation Cases | [x] 10/10 | [x] | [x] |

Scripts live in `library/series/series-01-optometry-foundations/season-03/` … `season-10/` as `SNNENN-<slug>.txt`. Season 8 header name spelled "Clinical Communication and Reasoning" (ampersand banned).

## 5b · Series 2 · "Ocular Anatomy for Optometrists" — scripted (100 episodes, 10 seasons × 10)

Deep, optometry-oriented anatomy: exactly how every ocular structure is built, connected, supplied and innervated.
Does NOT repeat Series 1 (no basic eye intro, basic visual concepts, basic terminology, or exam workflow).
Written by 10 batches × 10 agents, one agent per episode; every script PASS (`scripts/verify_ep.py`); every season E01 opener + E10 finale with next-season tease chain; every episode carries Series 1 + intra-series cross-references.

| Season | Title | Script | Rendered | In master.json |
|--------|-------|--------|----------|----------------|
| 01 | Orbit and Ocular Adnexa | [x] 10/10 | [x] | [x] |
| 02 | Lacrimal System | [x] 10/10 | [x] | [x] |
| 03 | Conjunctiva and Sclera | [x] 10/10 | [x] | [x] |
| 04 | Cornea | [x] 10/10 | [x] | [x] |
| 05 | Anterior Chamber and Uveal Tract | [x] 10/10 | [x] | [x] |
| 06 | Lens and Accommodation Anatomy | [x] 10/10 | [x] | [x] |
| 07 | Vitreous and Posterior Segment | [x] 10/10 | [x] | [x] |
| 08 | Retina, Choroid and Optic Nerve | [x] 10/10 | [x] | [x] |
| 09 | Extraocular Muscles and Ocular Movement | [x] 10/10 | [x] | [x] |
| 10 | Neuroanatomy for Optometrists | [x] 10/10 | [x] | [x] |

Scripts live in `library/series/series-02-ocular-anatomy-for-optometrists/season-01/` … `season-10/` as `SNNENN-<slug>.txt` (S-number = season within the series; series is distinguished by the folder, matching Series 1 convention).
Season titles in headers use "and" (ampersand banned); Episode 100 title written "Complete Visual Pathway - Retina to Cortex" (ASCII hyphen).

## 5c · Series 3 · "Ocular Physiology" — scripted (100 episodes, 10 seasons × 10)

How the normal eye and visual system actually function, building directly on Series 1 (foundations) and Series 2 (anatomy).
Explains NORMAL function only: no disease, diagnosis or treatment (later series own those); no anatomy re-teaching (Series 2 owns structure — recalled only by explicit back-reference).
Written by 10 batches × 10 agents, one agent per episode; every script PASS (`scripts/verify_ep.py`); 429,553 words ≈ 47.7 h audio; every season E01 opener + E10 finale with next-season tease chain; every episode carries Series 1 + Series 2 + intra-series cross-references.
Duplicate-title lane split: S6E6 Dark Adaptation and S6E7 Light Adaptation own photoreceptor photochemistry; S10E3 and S10E4 own the whole-system integrated view and bridge back explicitly.

| Season | Title | Script | Rendered | In master.json |
|--------|-------|--------|----------|----------------|
| 01 | Ocular Homeostasis | [x] 10/10 | [x] | [x] |
| 02 | Tear Film and Ocular Surface Physiology | [x] 10/10 | [x] | [x] |
| 03 | Corneal Physiology | [x] 10/10 | [x] | [x] |
| 04 | Aqueous and Intraocular Pressure | [x] 10/10 | [x] | [x] |
| 05 | Lens and Accommodation | [x] 10/10 | [x] | [x] |
| 06 | Retina Physiology | [x] 10/10 | [x] | [x] |
| 07 | Visual Physiology | [x] 10/10 | [x] | [x] |
| 08 | Colour and Contrast Vision | [x] 10/10 | [x] | [x] |
| 09 | Binocular and Oculomotor Physiology | [x] 10/10 | [x] | [x] |
| 10 | Visual Adaptation and Integration | [x] 10/10 | [x] | [x] |

Scripts live in `library/series/series-03-ocular-physiology/season-01/` … `season-10/` as `SNNENN-<slug>.txt` (matching Series 2 convention).
Season titles use "and" (ampersand banned); Episode 88 title written "Accommodation and Vergence Relationship" (en-dash replaced); ratios written in words ("the ratio that links accommodation to convergence") because the slash character is banned.

## 6 · Release tasks

- [x] Old 5-episode test batch deleted (scripts + rendered audio + catalog entries)
- [x] 20/20 scripts written and validated (Seasons 1-2)
- [x] Render Season 1 batch via workflow (run 37010813929, kokoro, all 10 episodes 28.4-31.6 min)
- [x] Render Season 2 batch via workflow (same run, all 10 episodes 25.4-29.4 min)
- [x] master.json shows 20 episodes with raw mp3 URLs (9.60 hours total, 24 kHz)
- [x] Demo renders (`rendered/demos/`) kept as engine samples only
- [x] 80/80 new scripts written and validated (Seasons 3-10) — 100/100 series total, all PASS
- [x] Render Seasons 3-10 via workflow (8 sequential season batches, kokoro, runs 37043823689 → 37063524360)
- [x] master.json shows 100 episodes, 45.47 hours total audio (24 kHz, raw mp3 URLs)
- [x] Series 1 Optometry Foundations COMPLETE: 10 seasons, 100 episodes, fully scripted and rendered
- [x] Series 2 100/100 scripts written and validated (10 seasons × 10, all PASS) + series.json bible
- [x] update_master.py upgraded to series-aware IDs (S<series>-S<season>E<ep>) — Series 2 would have collided 100/100 with Series 1
- [x] Render Series 2 run A: Seasons 1-4 (40 episodes) via workflow (run 37185937434; first attempt 37185392333 rendered only E01 - newline payload bug, fixed)
- [x] Render Series 2 run B: Seasons 5-7 (30 episodes) via workflow (run 37191005109)
- [x] Render Series 2 run C: Seasons 8-10 (30 episodes) via workflow (run 37195118235)
- [x] master.json shows 200 episodes (Series 1 + Series 2) with raw mp3 URLs
- [x] Series 2 Ocular Anatomy for Optometrists COMPLETE: 10 seasons, 100 episodes, 47.63 hours audio (24 kHz)
- [x] Focus Cast library total: 2 series, 200 episodes, 93.10 hours of audio
- [x] Series 3 100/100 scripts written and validated (10 seasons × 10, all PASS) + series.json bible
- [x] Render Series 3 via workflow (kokoro; runs 37226072850, 37228795037, 37232811938 S10 rerun, 37235404962, 37237989601, 37240489703, 37242882410, 37245160328, 37246991101, 37249415733; strict sequential dispatch after concurrency auto-cancel lesson; commit step rebases before push - fix 9d34927)
- [x] master.json shows 300 episodes (Series 1 + 2 + 3) with raw mp3 URLs
- [x] Series 3 Ocular Physiology COMPLETE: 10 seasons, 100 episodes, 48.96 hours audio (24 kHz)
- [x] Focus Cast library total: 3 series, 300 episodes, 142.06 hours of audio

## 7 · Series 1 roadmap (Seasons 3–10, planned — do NOT script before S1–S2 are rendered & locked)

- [x] Season 3 — Understanding Vision (scripted)
- [x] Season 4 — Optometric Terminology (scripted)
- [x] Season 5 — The Optometry Examination (scripted)
- [x] Seasons 6–10 — scripted (Basic Clinical Measurements, Prescriptions, Communication and Reasoning, Patient Journey, Foundation Cases)
