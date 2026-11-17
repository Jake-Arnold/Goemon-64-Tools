#!/usr/bin/env bash
# Run Japan-0 party unlock tests from the repository root.
# Read/write tests use synthetic guest RAM. They do not touch the live emulator.
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"

# Tk tests switch between Japan and USA. Prevent test run preferences
# (especially on_game_version_changed -> save_last_region) from modifying
# a real user's region/connection settings or affecting a later run.
TEST_CONFIG_HOME="$(mktemp -d "${TMPDIR:-/tmp}/goemon-ui-tests.XXXXXXXX")"
trap 'rm -rf -- "$TEST_CONFIG_HOME"' EXIT
export XDG_CONFIG_HOME="$TEST_CONFIG_HOME"

# Hidden modal confirmations in Xvfb can otherwise block indefinitely.
# This bounding applies only to the GUI smoke phase, not full ROM scans.
if ! command -v timeout >/dev/null 2>&1; then
  echo 'ERROR: GNU coreutils timeout is required to guard GUI smoke tests' >&2
  exit 2
fi
GUI_TIMEOUT_SECONDS="${GOEMON_GUI_TEST_TIMEOUT_SECONDS:-120}"
case "$GUI_TIMEOUT_SECONDS" in
  ''|*[!0-9]*) echo 'ERROR: GOEMON_GUI_TEST_TIMEOUT_SECONDS must be an integer' >&2; exit 2 ;;
esac

# Fail immediately with a clear syntax report for any practice module,
# including GUI files that might otherwise be imported late in test discovery.
"${PYTHON}" -m compileall -q practice
"${PYTHON}" -m scripts.sync_address_catalogue --write
"${PYTHON}" -m scripts.sync_address_catalogue --check

"${PYTHON}" -m unittest \
  tests.test_japanese_fields \
  tests.test_japanese_scene_probes \
  tests.test_japanese_party_unlock \
  tests.test_japanese_position \
  tests.test_japanese_debug_warp \
  tests.test_japan_debug_menu_controller \
  tests.test_japan_position_controller \
  tests.test_japan_party_cli \
  tests.test_japan_party_controller \
  tests.test_japanese_mupen_attach \
  tests.test_japan_native_recomp \
  tests.test_japan_auto_attach \
  tests.test_japan_pid_restart_watch \
  tests.test_gui_smoke_runner \
  tests.test_toolkit_version \
  tests.test_updater \
  tests.test_linux_launcher \
  tests.test_launcher_preferences \
  tests.test_japan_project64 \
  tests.test_remembered_rom \
  tests.test_region_views \
  tests.test_story_progress \
  tests.test_plasma_conditions \
  tests.test_japan_story_progress \
  tests.test_native_checkpoints \
  tests.test_region_unlocks \
  tests.test_unlock_flag_catalog \
  tests.test_address_registry \
  tests.test_address_metadata_sync \
  tests.test_region_memory_crosswalk \
  tests.test_region_crosswalk_agent \
  tests.test_crosswalk_shared_pages \
  tests.test_rom_layout_audit \
  tests.test_rom_context_audit \
  tests.test_japan_live_memory_edit \
  tests.test_japan_value_freezes \
  tests.test_value_freezes \
  tests.test_japan_event_sessions \
  tests.test_japan_damage_capture \
  tests.test_japan_native_scene_warp \
  tests.test_japan_direct_scene_reload \
  tests.test_japan_warp_spawns \
  tests.test_japan_spawn_placement \
  tests.test_known_entrances \
  tests.test_repository_entrance_atlas \
  tests.test_japan_native_scene_controller \
  tests.test_japan_scene_readiness \
  tests.test_japan_state_comparison \
  tests.test_japan_player_position_research \
  tests.test_value_search \
  tests.test_reports \
  tests.test_discovery_results \
  tests.test_state_discovery \
  -v

if [[ -n "${GOEMON_USA_DECOMPRESSED:-}" && -n "${GOEMON_JAPAN_DECOMPRESSED:-}" ]]; then
  "${PYTHON}" -m practice.rom_layout_audit \
    --usa "${GOEMON_USA_DECOMPRESSED}" \
    --japan "${GOEMON_JAPAN_DECOMPRESSED}" --summary
  if [[ "${GOEMON_ROM_CONTEXT_AUDIT:-}" == '1' ]]; then
    "${PYTHON}" -m practice.rom_context_audit \
      --usa "${GOEMON_USA_DECOMPRESSED}" \
      --japan "${GOEMON_JAPAN_DECOMPRESSED}" --summary
  fi
fi

if command -v xvfb-run >/dev/null 2>&1; then
  xvfb-run -a timeout --signal=TERM --kill-after=5s "${GUI_TIMEOUT_SECONDS}s" "${PYTHON}" -m tests.gui_smoke_runner \
    tests.test_japanese_fields_ui \
    tests.test_japanese_scene_probe_ui \
    tests.test_japanese_party_controls_ui \
    tests.test_japanese_position_ui \
    tests.test_japanese_debug_ui \
    tests.test_japan_event_sessions_ui \
    tests.test_japan_readonly_parity \
    tests.test_japan_state_comparison_ui \
    tests.test_value_search_ui \
    tests.test_reports_ui \
    tests.test_discovery_reports_ui \
    tests.test_discovery_results_ui \
    tests.test_toolkit_redundancy_ui \
    tests.test_state_discovery_ui \
    tests.test_region_unlocks_ui \
    tests.test_unlock_flags_ui \
    tests.test_address_catalogue_ui \
    tests.test_japan_story_progress_ui \
    tests.test_japan_named_checkpoint_ui \
    tests.test_japan_value_freezes_ui \
    tests.test_value_freezes_ui \
    tests.test_story_progress_ui \
    tests.test_dashboard \
    tests.test_updater_ui \
    tests.test_entrance_ui \
    tests.test_japan_recomp_write_ui \
    -v
elif [[ -n "${DISPLAY:-}" ]]; then
  timeout --signal=TERM --kill-after=5s "${GUI_TIMEOUT_SECONDS}s" "${PYTHON}" -m tests.gui_smoke_runner \
    tests.test_japanese_fields_ui \
    tests.test_japanese_scene_probe_ui \
    tests.test_japanese_party_controls_ui \
    tests.test_japanese_position_ui \
    tests.test_japanese_debug_ui \
    tests.test_japan_event_sessions_ui \
    tests.test_japan_readonly_parity \
    tests.test_japan_state_comparison_ui \
    tests.test_value_search_ui \
    tests.test_reports_ui \
    tests.test_discovery_reports_ui \
    tests.test_discovery_results_ui \
    tests.test_toolkit_redundancy_ui \
    tests.test_state_discovery_ui \
    tests.test_region_unlocks_ui \
    tests.test_unlock_flags_ui \
    tests.test_address_catalogue_ui \
    tests.test_japan_story_progress_ui \
    tests.test_japan_named_checkpoint_ui \
    tests.test_japan_value_freezes_ui \
    tests.test_value_freezes_ui \
    tests.test_story_progress_ui \
    tests.test_dashboard \
    tests.test_updater_ui \
    tests.test_entrance_ui \
    tests.test_japan_recomp_write_ui \
    -v
else
  echo 'ERROR: Tk smoke tests need xvfb-run (sudo apt install xvfb xauth)' >&2
  exit 2
fi
