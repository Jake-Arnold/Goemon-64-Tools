"""Stage the reviewed collision-gate C replacement in a separate file.

This is source preparation only; it does not compile, link, or verify a ROM.
"""
import argparse
from pathlib import Path

from .collision_patch import prepare_collision_gate


def stage_collision_gate(upstream: Path, candidate: Path, output: Path) -> Path:
    """Validate before exclusive creation; never overwrite any source file."""
    upstream = Path(upstream)
    candidate = Path(candidate)
    output = Path(output)
    if output.resolve() in (upstream.resolve(), candidate.resolve()):
        raise ValueError('Output must differ from both source inputs')
    # Read bytes and decode strictly: newline conversion would change the
    # compiler input, and the source-hash guard must see the original LF bytes.
    original = upstream.read_bytes().decode('utf-8')
    reviewed = candidate.read_bytes().decode('utf-8')
    transformed = prepare_collision_gate(original, reviewed)
    with output.open('xb') as handle:
        handle.write(transformed.encode('utf-8'))
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    stage_collision_gate(args.upstream, args.candidate, args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
