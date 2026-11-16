"""Find script set/clear pattern candidates for Plasma's checked/set flags."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from decomp.plasma_conditions import extract
from practice.rom_flag_trace import analyze_rom


def extract_writers(data):
    plasma=extract(data)
    ids=sorted({int(op['flag_id'],16) for op in plasma['operations']})
    # analyze_rom requires the verified decompressed ROM; it does not claim a
    # complete native-code scan or prove that aligned data is executable script.
    report=analyze_rom(data,ids)
    writers=[row for row in report['references'] if row['operation'] in ('set','clear')]
    return dict(format='goemon-plasma-writers-v1',rom_sha1=report['rom_sha1'],
                flag_ids=[f'0x{value:03X}' for value in ids],writers=writers,
                limitation='Script opcode-pattern candidates only; no native scan, reachability or actor binding established')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',type=Path,required=True,help='Verified decompressed US ROM')
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        if args.rom.resolve()==args.report.resolve():raise ValueError('Report must differ from ROM')
        result=extract_writers(args.rom.read_bytes())
        with args.report.open('x',encoding='utf-8') as stream:
            json.dump(result,stream,indent=2);stream.write('\n')
    except (OSError,ValueError) as exc:parser.exit(1,f'{exc}\n')
    print(f"{len(result['flag_ids'])} flags / {len(result['writers'])} script writer candidates")

if __name__=='__main__':main()
