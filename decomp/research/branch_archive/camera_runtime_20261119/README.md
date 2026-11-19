# Historical USA camera-mode and reset research (research only)

Source branches and audited head SHAs:
- `chatgptweb/camera-mode-runtime-audit-20261116` @ `73b822de4a159d3794b86f1bd53d0d3bf6805034`
- `chatgptweb/camera-reset-136-native-20261116` @ `c95975b28533b114acd65eb0d92b28405ae1ac01`
- `chatgptweb/camera-reset-343-scratch-20261117` @ `c14f403b6c01ae295e9ff04313705871452468ab`
- `chatgptweb/camera-reset-343-integration-20261117` @ `66a7ad5516f3f0a8b3abc30d1cbf8a42c19b781e`

Files absent from both canonical branches are preserved byte-for-byte below this directory, with original repository-relative path suffixes. No active production code, manifest, accepted C, ROM, or ELF proof modified. Early 136-byte camera reset research (including the 343-file11 stage) is historical and **not** a new verification of current 1,500-USA-C / 432-JP-C canon. No tests were rerun for this archive.

- `decomp/results/usa_camera_runtime_trace_20261116.json` ← `chatgptweb/camera-mode-runtime-audit-20261116` (`efb1bb1630dab386ef002ca60c1abb8bfe42e99c`)
- `docs/USA_CAMERA_MODE_RUNTIME_AUDIT_2026-11-16.md` ← `chatgptweb/camera-mode-runtime-audit-20261116` (`6ead4d5863fd760d9d4f51cbf106c4cff60bea97`)
- `tests/test_decomp_camera_runtime_evidence.py` ← `chatgptweb/camera-mode-runtime-audit-20261116` (`e3b258a2a7394d58423fe4662744594b8e81b581`)
- `decomp/research/camera_reset_136_probe.py` ← `chatgptweb/camera-reset-136-native-20261116` (`e6cf094086505fb08819cee123ba8f4c35d2c248`)
- `decomp/results/camera_reset_136_native_research_20261116.json` ← `chatgptweb/camera-reset-136-native-20261116` (`6dd32bb7aee0fdd45613264033bf7984ba50b599`)
- `docs/USA_CAMERA_RESET_136_MATCHING_C_2026-11-16.md` ← `chatgptweb/camera-reset-136-native-20261116` (`651d30db6ad8e1d6492a9ef44405511dfee1db47`)
- `tests/test_decomp_camera_reset_136.py` ← `chatgptweb/camera-reset-136-native-20261116` (`ae784d7985d6ae1bfb7fa931c83af1b1584c5fcb`)
- `decomp/results/camera_reset_136_scratch_proof_20261117.json` ← `chatgptweb/camera-reset-343-scratch-20261117` (`e653840e1a8b7eab8ccfabf5f53977c5284b045b`)
- `docs/USA_CAMERA_RESET_136_SCRATCH_20261117.md` ← `chatgptweb/camera-reset-343-scratch-20261117` (`3e3f55083d480bdcf5c78ce1ef3b59245f6e9c5b`)
- `tests/test_decomp_camera_reset_scratch_20261117.py` ← `chatgptweb/camera-reset-343-scratch-20261117` (`5d7b528dcaee62cb6911af191e27d859adc578f5`)
- `decomp/candidates/manifest_camera_343_20261117.json` ← `chatgptweb/camera-reset-343-integration-20261117` (`bda59f1bcd12d0e898d967112877aafbab25c6ef`)
- `decomp/file11_180_stage.py` ← `chatgptweb/camera-reset-343-integration-20261117` (`7b3823b8c92ac5961f4528f4275efcecb45b5733`)
- `docs/USA_CAMERA_RESET_343_INTEGRATION_20261117.md` ← `chatgptweb/camera-reset-343-integration-20261117` (`87e274ae91162a48a089efdb87454bdc99387331`)
- `tests/test_decomp_file11_180_stage.py` ← `chatgptweb/camera-reset-343-integration-20261117` (`6484c6e00610bf6fe954399ff5036dfc909b26bc`)

Unresolved multiple historic blob versions: 0. Preserve alternate files before deletion where differences are material.
