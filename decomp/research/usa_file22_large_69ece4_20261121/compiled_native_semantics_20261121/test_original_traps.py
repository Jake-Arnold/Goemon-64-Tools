#!/usr/bin/env python3
"""Exercise original compiler-emitted divide guards in isolated MIPS harness.
These are invalid/synthetic inputs; never use a patched ROM in a real game.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from trace_original_file22_mips import prepare,OriginalMIPS,SAVED_DESC

FIELDS=(('page_width_zero',0x20,'0x801cc270'),
        ('page_height_zero',0x22,'0x801cc2cc'),
        ('page_columns_zero',0x1c,'0x801cc294'),
        ('page_rows_zero',0x1e,'0x801cc2f4'))

def run(rom):
 reports=[]
 for name,off,pc in FIELDS:
    ram=prepare(rom,2)
    ram.store(SAVED_DESC+off,0,2)
    cpu=OriginalMIPS(ram)
    try:cpu.run()
    except ArithmeticError as e:
       actual=str(e).rsplit(' ',1)[-1]
       if actual != pc:raise AssertionError(f'Wrong original guard for {name}: {actual} expected {pc}')
       reports.append({'case':name,'expected_break_pc':pc,'observed_break_pc':actual,'pass':True,
                       'original_instructions_until_trap':cpu.executed})
    else:raise AssertionError(f'Original guard missing for {name}')
 return reports

def main():
 p=argparse.ArgumentParser();p.add_argument('--rom',required=True,type=Path);p.add_argument('--output',type=Path)
 args=p.parse_args();x=run(args.rom.read_bytes())
 if args.output:args.output.write_text(json.dumps(x,indent=2)+'\n')
 print(json.dumps(x,indent=2))
if __name__=='__main__':main()
