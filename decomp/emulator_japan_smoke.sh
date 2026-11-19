#!/usr/bin/env bash
# Goemon Japan 329-C runtime smoke test for Linux/X11, using Mupen64Plus.
# Capture screenshots, emulator logs and attempted START/A/analog input.
# A screenshot is evidence to inspect, NOT automatic proof of gameplay.
set -Eeuo pipefail
EXPECTED=9843ee979b5f6c80f5eda85df0baed9ae7c4e73b
usage() {
  echo "Usage: $0 <rebuilt-japan-retail.z64> <reference-japan-normalized.z64> <output-directory>" >&2
  exit 2
}
if [[ "${1:-}" == --inside ]]; then
  [[ $# -eq 3 ]] || usage
  rom=$2
  out=$3
  export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 LIBGL_ALWAYS_SOFTWARE=1
  emulator_pid=''
  cleanup() {
    if [[ -n "$emulator_pid" ]]; then
      kill "$emulator_pid" 2>/dev/null || true
      wait "$emulator_pid" 2>/dev/null || true
    fi
  }
  trap cleanup EXIT
  timeout --signal=TERM --kill-after=5s 160s mupen64plus --nosaveoptions "$rom" >"$out/emulator.log" 2>&1 &
  emulator_pid=$!
  echo "Emulator PID $emulator_pid; display $DISPLAY" >> "$out/steps.log"
  win=''
  for _ in $(seq 1 40); do
    if ! kill -0 "$emulator_pid" 2>/dev/null; then
      echo 'BLOCKED_EMULATOR: emulator exited before window appeared' >> "$out/steps.log"
      exit 5
    fi
    win=$(xdotool search --onlyvisible --name 'Mupen64Plus|mupen64plus|Goemon|GANBARE' 2>/dev/null | head -1 || true)
    [[ -n "$win" ]] && break
    sleep 1
  done
  if [[ -z "$win" ]]; then
    echo 'BLOCKED_EMULATOR: no visible emulator window found' >> "$out/steps.log"
    exit 5
  fi
  echo "Emulator window ID $win" >> "$out/steps.log"
  xdotool windowfocus --sync "$win" 2>> "$out/steps.log" || true
  capture() {
    local filename=$1
    if ! kill -0 "$emulator_pid" 2>/dev/null; then
      echo "EMULATOR_EXITED_BEFORE_${filename}" >> "$out/steps.log"
      exit 5
    fi
    ffmpeg -hide_banner -nostdin -loglevel error -y \
      -f x11grab -video_size 1024x768 -i "$DISPLAY" -frames:v 1 "$out/${filename}.png" \
      >> "$out/capture.log" 2>&1
    echo "CAPTURED_${filename}" >> "$out/steps.log"
  }
  sleep 8
  capture boot
  sleep 12
  capture title_or_intro
  for _ in 1 2 3; do
    xdotool key --window "$win" --clearmodifiers Return
    sleep 2
  done
  sleep 6
  capture after_start
  for _ in 1 2 3 4 5 6; do
    xdotool key --window "$win" --clearmodifiers Shift_L
    sleep 2
  done
  capture after_a
  xdotool keydown --window "$win" Right
  sleep 3
  xdotool keyup --window "$win" Right
  xdotool keydown --window "$win" Up
  sleep 3
  xdotool keyup --window "$win" Up
  sleep 5
  capture after_movement_attempt
  echo 'INPUT_ATTEMPTED: Start x3, A x6, Right/Up; visually inspect screenshots for game/title/gameplay' >> "$out/steps.log"
  exit 0
fi
[[ $# -eq 3 ]] || usage
for cmd in sha1sum cmp realpath xvfb-run mupen64plus xdotool ffmpeg timeout; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "BLOCKED_INPUT: missing dependency: $cmd" >&2
    exit 4
  fi
done
rom=$(realpath -e -- "$1")
reference=$(realpath -e -- "$2")
out=$(realpath -m -- "$3")
mkdir -p "$out"
printf 'GOEMON JP RUNTIME SMOKE\nCompiled ROM: %s\nReference ROM: %s\n' "$rom" "$reference" > "$out/steps.log"
romsha=$(sha1sum "$rom" | cut -d ' ' -f1)
refsha=$(sha1sum "$reference" | cut -d ' ' -f1)
if [[ "$romsha" != "$EXPECTED" || "$refsha" != "$EXPECTED" ]] || ! cmp -s -- "$rom" "$reference"; then
  echo "BLOCKED_ROM: JP retail ROM mismatches reference. built=$romsha reference=$refsha" | tee -a "$out/steps.log" >&2
  exit 3
fi
echo "ROM_EXACT_MATCH: sha1=$EXPECTED" >> "$out/steps.log"
if xvfb-run -a -s '-screen 0 1024x768x24' bash "$0" --inside "$rom" "$out"; then
  sha256sum "$out"/*.png > "$out/screenshots.sha256"
  echo 'SMOKE_CAPTURE_COMPLETED: emulator ran and input was attempted; gameplay requires visual review.' | tee -a "$out/steps.log"
else
  echo 'BLOCKED_EMULATOR: inspect emulator.log, capture.log, and steps.log' | tee -a "$out/steps.log" >&2
  exit 5
fi
