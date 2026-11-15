# Native emulator savestates

The Dashboard now exposes **Full emulator savestates** (slot 0–9; Save F5 / Load F7). Unlike the former logical checkpoint, this delegates serialization to Project64 or the Mupen64Plus core rather than copying only selected guest-RAM values.

**Scope and limitations:** Project64 and Mupen64Plus support this native-hotkey adapter. The toolkit still has USA live memory for Goemon64Recomp and the earlier Project64 integration. Mupen64Plus has new savestate-only process selection: the toolkit makes no claim that its RAM mapping works. The Goemon64Recomp runtime has no verified complete-savestate API; selecting Recomp explicitly rejects the request.

Use the Connection dropdown to select Project64, Mupen64Plus, or auto. Provide an optional PID, or let the toolkit locate one unambiguous emulator. Pick a state slot and use Save/Load. The actual state format and files belong to the emulator; check its OSD to confirm completion. Standard bindings are required: numeric slot selection, F5 save, F7 load. A requested hotkey is NOT proof that an emulator completed saving.

**Supported host input:** Windows requires a visible window for the exact emulator PID; the adapter requests foreground focus, re-verifies the foreground PID, and then sends the keys. Linux requires an X11/Xorg desktop and xdotool with visible PID-owned windows. Wayland and macOS are not supported by this method. Read-only mode blocks the shortcuts. This path cannot verify which ROM an emulator has currently loaded, so do not assume a selected version identifies an emulator session.

Before a native save/load, the toolkit stops its own freezes and pending write sessions. Before load, it also discards its live RDRAM handle because actors/pointers become stale after restoring a state. Reconnect to inspect RAM after loading.

The old logical checkpoint card is hidden rather than deleting existing JSON checkpoints or its Python functions. No legacy checkpoint is converted into a native savestate.

Japanese releases can be played and saved by a compatible emulator independently of Goemon64Recomp. Japanese live-RAM tools remain disabled until validated. Complete savestates in Goemon64Recomp require runtime-level thread, scheduler, timer, messages, overlay, audio and renderer-state serialization and restoration; an 8-MiB RAM dump alone is insufficient.

Mocked test cases are in tests/test_emulator_savestates.py and tests/test_dashboard.py. No real emulator or full GUI integration test has been run from the GitHub connector environment.
