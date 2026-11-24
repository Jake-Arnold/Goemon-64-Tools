#!/usr/bin/env bash
# Private original-ROM replay of the accepted JP2118 -> JP2528 stages and JP6.
# Each native historical stage still runs its own build/verify gate; redundant
# historical ROM-free CI invocations are deferred to a single full candidate CI.
# No promotion or repository files are written by this driver.
set -euo pipefail
if (( $# != 7 )); then echo 'usage: replay_jp6_from_2118.sh <verified JP2118 checkout> <pristine JP6 split> <original native100 split> <deps> <runtime> <uv adapter> <new private work dir>' >&2; exit 2; fi
co=$(realpath "$1"); pristine=$(realpath "$2"); native_reference=$(realpath "$3"); deps=$(realpath "$4"); runtime=$(realpath "$5"); uv=$(realpath "$6"); work=$(realpath -m "$7")
repo=$(cd "$(dirname "$0")/../../.." && pwd)
[[ ! -e "$work" ]]; mkdir -p "$work"
export PATH="$deps/bin:$PATH" LD_LIBRARY_PATH="$runtime/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" UV="$uv"
export GOEMON_JOBS=${GOEMON_JOBS:-4}
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH python3 -m "decomp.$1" "${@:2}")
snapshot() { mkdir -p "$work/$1/build/japan_0"; cp "$co/build/japan_0/mnsg.elf" "$co/build/japan_0/mnsg.z64" "$work/$1/build/japan_0/"; }
retail() {
  (cd "$co"; env PYTHONHOME="$runtime/python" PYTHONPATH="$deps/.venv/lib/python3.12/site-packages" LD_LIBRARY_PATH="$runtime/lib" "$runtime/python/bin/python3.12" tools/rommy.py compress --input build/japan_0/mnsg.z64 --output "$work/$1.retail.z64" --manifest config/japan_0/rommy.yaml --pad --verify >/dev/null)
  cmp "$work/$1.retail.z64" "$co/config/japan_0/baserom.z64"; rm "$work/$1.retail.z64"
}
# Revalidate the supplied JP2118 native baseline before any mutation.
run japan_1686_promotion verify --checkout "$co" --deps "$deps" --runtime "$runtime"
retail jp2118
snapshot jp2118
run glitch_g2_promotion stage --checkout "$co" --region japan_0
run glitch_g2_promotion build --checkout "$co" --region japan_0 --deps "$deps" --runtime "$runtime"
run glitch_g2_promotion verify --checkout "$co" --region japan_0 --baseline "$work/jp2118"
snapshot jp2121
run vm_g2_promotion stage --checkout "$co"
run vm_g2_promotion build --checkout "$co" --deps "$deps" --runtime "$runtime"
run vm_g2_promotion verify --checkout "$co" --baseline "$work/jp2121"
snapshot jp2123
stage() {
  local module=$1 prior=$2 result=$3
  run "$module" stage --checkout "$co"
  run "$module" build --checkout "$co" --deps "$deps" --runtime "$runtime"
  run "$module" verify --checkout "$co" --base "$work/$prior"
  retail "$result"; snapshot "$result"
  printf 'Verified historical native stage %s\n' "$result"
}
stage japan_short145_promotion jp2123 jp2268
stage japan_donor10_promotion jp2268 jp2278
stage japan_donor4_promotion jp2278 jp2282
stage japan_tiny7_promotion jp2282 jp2289
stage japan_retry29_promotion jp2289 jp2303
stage japan_retry10_promotion jp2303 jp2307
stage japan_expand7_promotion jp2307 jp2314
run japan_jp55_promotion plan --checkout "$co"
stage japan_jp55_promotion jp2314 jp2369
cp -a "$co" "$work/original2369"
run japan_cright_promotion stage --checkout "$co"
run japan_cright_promotion build --checkout "$co" --deps "$deps" --runtime "$runtime"
# Independently assemble original source with the already-reviewed historical
# C-Right relocation provenance distinction; never derive it from candidate C.
cp -a "$co" "$work/shadow2369"
run japan_cright_dual_reference shadow-stage --shadow "$work/shadow2369"
run japan_cright_dual_reference shadow-build --shadow "$work/shadow2369" --deps "$deps" --runtime "$runtime"
run japan_cright_dual_reference verify --original "$work/original2369" --shadow "$work/shadow2369" --candidate "$co" --report "$work/jp2370-dual.json"
retail jp2370; snapshot jp2370
stage japan_short28_promotion jp2370 jp2398
stage japan_crossregion30_promotion jp2398 jp2428
run native251_promotion --region japan_0 --checkout "$co" --pristine "$native_reference" --work "$work/jp2528-native" --uv "$uv" --jobs "$GOEMON_JOBS"
retail jp2528; snapshot jp2528
run japan_cright6_promotion --checkout "$co" --pristine "$pristine" --work "$work/jp2534" --uv "$uv" --jobs "$GOEMON_JOBS"
printf '%s\n' 'Native replay only; candidate integrity and full local CI still mandatory.'
