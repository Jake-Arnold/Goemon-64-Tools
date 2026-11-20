# Japan-0 Dialogue Editor — original-ROM evidence and release limits

Date: 19 November 2026. Repository target: `toolkit/dialogue-explorer-20261119`.

## Source ROM identities

| Image | Size | SHA-1 |
| --- | --- | --- |
| USA retail `.z64` | 16 MiB | `df8083a54296b8c151917c5333e1c85f014a2a66` |
| USA decompressed `.z64` | 32 MiB | `6ea0ed71032ce08fc2745f412d84936382197494` |
| Japan-0 retail, original byte-swapped `.n64` (actually v64 magic) | 16 MiB | `b6386455c0b8f573e315976bbb47548cbafcedb3` |
| Japan-0 retail, normalised big endian `.z64` | 16 MiB | `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` |
| Japan-0 decompressed `.z64` | 32 MiB | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |

The Japanese original `.n64` begins with `37 80 40 12`. Swap adjacent byte pairs to obtain `80 37 12 40` and verify the normalised SHA-1; file extensions must not decide byte order.

## Japan resource and VM evidence

`Nisitenma-Ichigo` is at decompressed image offset `0x58248` (USA: `0x57FC8`). Japan file-table offset `0x58258`; paired eight-byte virtual-range table `0x5594C`, fixed 1,312 file entries plus zero terminator. First decompressed data file `0x57C5F0`, last real endpoint `0x14B3C40`. The same-source text command consists of word `0x8010` followed by a word containing a virtual operand, pointing to signed big-endian 16-bit token stream ending in sentinel `-1`. Resource 81, 82, 93, 96, 97 samples confirm the same control split and segment 8 base used for many scripts.

A strictly aligned static candidate search finds 5,039 distinct referenced text records across 42 resources, linked from 5,694 `0x8010` sites. A **candidate is not a proven reachable script node**. In particular, computed pointers and dynamic/generated RAM text are not enumerated.

The Japanese script token alphabet differs drastically from USA: 313 distinct nonnegative token IDs are observed among the candidate records, with observed maximum token 395. No proven complete kana/kanji Unicode mapping is presently available. The editor therefore **must not apply the USA ASCII glyph mapping**. Japan-0 mode uses explicit signed `<token:N>` entries, preserving the known N64 control names and `-60` newline convention; token 13 is displayed as space because repeated indentation patterns support that reading, but it round-trips to the same numeric value. These IDs are not Shift-JIS code points. Ordinary Japanese Unicode input is refused rather than guessed. Auto-wrapping, USA-native width tables and USA window dimensions are not reused for Japanese text.

## Retail repack proof

The original Japanese retail decompressed resource table can be transformed into its original compressed form with the `lzkn64==0.2.0` module, preserving each resource's original bit-31 compression flag, padding compressed blocks to even-byte boundaries, rewriting the compressed table offsets and recomputing CIC-6102 header checksums. The **unmodified** repack is byte-for-byte identical to the normalised Japanese retail image (SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`). The bootcode CRC-32 over bytes `0x40..0xFFF` is `90BB6CB5`, matching the USA CIC-6102 configuration. A modified same-length token and a variable-length relocated token record in resource 82 both produced bounded 16 MiB repacked images. No live Project64/Mupen gameplay evidence was collected for these Japanese edits.

The editor requires the pinned original as an input. It refuses unrecognised revisions, previously modified ROMs, changed control-token sequences, inconsistent resource offsets, resource growth above `0x4000`, and output writes over any original source image. Japanese text pointer relocation updates statically discovered same-resource references only. Original records are preserved as fallback for untraced readers.

## Persistent library and drag-and-drop

ROMs are not committed, downloaded automatically or embedded in the Toolkit. After **user-initiated import**, a verified original is copied into a per-user data directory (`$XDG_DATA_HOME/GoemonSpeedrunTools/dialogue-roms` on Linux, `%LOCALAPPDATA%\GoemonSpeedrunTools\dialogue-roms` on Windows, and the Application Support directory on macOS). Importing a 16 MiB original decompresses it once and stores both original big-endian retail and pinned 32 MiB decompressed images. Every subsequent reuse rehashes the stored image, and corrupt/missing assets are rejected. There is no dependency on emulator connection or a remembered live-game PID.

The Toolkit root uses `tkinterdnd2` when present, exposing native TkDND file-drop handling; the browse/import button remains available if TkDND cannot load. File-drop Tcl lists are parsed without shell invocation. The **Open built ROM directory** button opens the last successful build's folder (or the persistent default `dialogue-roms/built/` directory). Linux uses `xdg-open`, Windows `os.startfile`, and macOS `open`, without shell interpolation.

## Tests and outstanding proof

Local test run: original pinned USA/Japan images; portable Python 3.12.16, `lzkn64` 0.2.0, and Xvfb Tk: 18 new functional tests passed, no skips. Tests checked source normalisation, original repack byte equality, both auto-decompression paths, a real resource 82 edited token, longer-token relocation, safe source-write refusal, persistent library corruption handling, native Tk fallback and file-manager dispatch. The entire existing Toolkit regression and installed real TkDND package were **not** exercised in this run.

Pending: map the Japanese glyph atlas and Unicode conversion; verify modified Japanese display and title compatibility in Project64; verify real TkDND under both Linux/Windows; full toolkit regression; static script-graph coverage and Japanese font/window measurements.
