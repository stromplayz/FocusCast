#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# TTS Beta FL — one-command episode renderer for GitHub Codespaces.
#
# The "Codespaces loophole": GitHub gives personal accounts 120 free
# core-hours per month. Spin up a 4-core codespace, render the episode on
# Microsoft's machines, then just commit the finished audio back to the repo.
# Zero local GPU. Zero paid compute. 100% inside GitHub.
#
# Usage:
#   bash scripts/run_codespace.sh                       # default episode
#   bash scripts/run_codespace.sh scripts/episodes/foo.txt
#   TTS_MODEL_ID=openbmb/VoxCPM2 bash scripts/run_codespace.sh
# ---------------------------------------------------------------------------
set -euo pipefail

EPISODE="${1:-scripts/episodes/retina.txt}"
[ $# -gt 0 ] && shift
EXTRA=("$@")

mkdir -p output

echo "==> TTS Beta FL · Codespace renderer"
echo "==> episode : ${EPISODE}"
echo "==> model   : ${TTS_MODEL_ID:-openbmb/VoxCPM-0.5B}"
echo "==> cores   : $(nproc)"
echo

python scripts/generate_tts.py \
  --episode "${EPISODE}" \
  --engine voxcpm \
  --model-id "${TTS_MODEL_ID:-openbmb/VoxCPM-0.5B}" \
  --timesteps "${TTS_TIMESTEPS:-8}" \
  --cfg "${TTS_CFG:-2.0}" \
  --outdir output \
  ${EXTRA[@]+"${EXTRA[@]}"}

echo
echo "==> Render finished:"
ls -lh output/

cat <<'TIP'

==> Next step — save the audio into the repo:
      git add output/
      git commit -m "feat(audio): episode rendered in Codespaces"
      git push
TIP
