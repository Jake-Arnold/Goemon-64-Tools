#!/usr/bin/env python3
"""Research: compare authentic USA-original and native IDO emitted MIPS visible LOAD and STORE sequences.

User must supply the pinned original decompressed ROM and compiler-produced object.
Only metadata reports are written: no original code, ROM bytes or memory dumps.
Synthetic guest RAM experiments are not real hardware execution.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,sys
from pathlib import Path

from reproduce_compiled_ido import compiled_guest_text, cases, FUN_SHA256
from dual_region_native_probe import geometry_cases
import trace_original_file22_mips as trace


def run(rom,code,mode,rows=None,layout=None,alias=None,zero_dim=None):
    ram=trace.prepare(rom,mode,rows,layout)
    if alias:
        kind,offset=alias
        field={'pagemap':4,'tilemap':8,'texdesc':12}[kind]
        ram.store(trace.SAVED_DESC+field,trace.OUTPUT+offset)
    if zero_dim is not None:ram.store(trace.SAVED_DESC+zero_dim,0,2)
    if code:
        block,p=ram.block(trace.ENTRY,len(code));block[p:p+len(code)]=code
    loads=[];stores=[];stack_reads=[];stack_writes=[]
    read=ram.load;store=ram.store
    end=trace.ENTRY+(len(code) if code else trace.END-trace.ENTRY)
    def observe_load(addr,n=4,signed=False):
        v=read(addr,n,signed)
        if not trace.ENTRY<=addr<end:  # exclude opcode fetch; still include texture/data accesses
            event=(addr,n,v)
            if trace.STACK<=addr<trace.STACK+0x2000:stack_reads.append(event)
            else:loads.append(event)
        return v
    def observe_store(addr,value,n=4):
        store(addr,value,n)
        event=(addr,n,value&((1<<(8*n))-1))
        if trace.STACK<=addr<trace.STACK+0x2000:stack_writes.append(event)
        else:stores.append(event)
    ram.load=observe_load;ram.store=observe_store
    cpu=trace.OriginalMIPS(ram)
    oldend=trace.END
    try:
        if code:trace.END=trace.ENTRY+len(code)
        try:cpu.run(limit=250000)
        except Exception as e:return {'status':type(e).__name__,'error':str(e)[:100],'pc':cpu.pc,'executed':cpu.executed,
                                      'loads':loads,'stores':stores,'stack_loads':len(stack_reads),'stack_stores':len(stack_writes)}
    finally:trace.END=oldend
    # Bypass observed ram.load for final inspection.
    ptr=read(trace.CURSOR)
    if not trace.OUTPUT<=ptr<=trace.OUTPUT+65536 or (ptr-trace.OUTPUT)%8:raise ValueError('Output buffer exceeded')
    gfx=bytes(ram.block(trace.OUTPUT,ptr-trace.OUTPUT)[0][:ptr-trace.OUTPUT])
    return {'status':'OK','executed':cpu.executed,'loads':loads,'stores':stores,'gfx':gfx,
            'stack_loads':len(stack_reads),'stack_stores':len(stack_writes)}

def summarize_case(key,org,cand,expected_status=None):
    row={'case':key,'original_status':org['status'],'compiled_status':cand['status']}
    if expected_status=='MemoryError':
        row['excluded_from_pass_count']=True
        if org['status']!='MemoryError' or cand['status']!='MemoryError':raise AssertionError(f'Error inventory drift {key}: {row}')
        return row
    if org['status']!='OK' or cand['status']!='OK':raise AssertionError(f'Successful case now fails {key}: {row}')
    row.update({'original_external_reads':len(org['loads']),'compiled_external_reads':len(cand['loads']),
        'original_external_writes':len(org['stores']),'compiled_external_writes':len(cand['stores']),
        'read_order_equal':org['loads']==cand['loads'],'write_order_equal':org['stores']==cand['stores'],
        'gfx_equal':org['gfx']==cand['gfx'],'gfx_commands':len(org['gfx'])//8,
        'original_stack_loads':org['stack_loads'],'compiled_stack_loads':cand['stack_loads'],
        'original_stack_stores':org['stack_stores'],'compiled_stack_stores':cand['stack_stores']})
    if not all((row['read_order_equal'],row['write_order_equal'],row['gfx_equal'])):
        raise AssertionError(f'Observable difference in {key}: {row}')
    return row

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--usa',required=True,type=Path)
    p.add_argument('--object',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    if a.output.exists():raise FileExistsError('Use a fresh report path')
    rom=a.usa.read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=trace.ROM_SHA1:raise ValueError('Original decompressed USA ROM SHA1 mismatch')
    if hashlib.sha256(rom[0x69ECE4:0x69F3F4]).hexdigest()!=FUN_SHA256:raise ValueError('Function hash mismatch')
    code=compiled_guest_text(a.object)
    report={'format':'file22-original-ido-visible-load-store-order-v1',
      'status':'RESEARCH_ONLY_NOT_NATIVE_EXACT','original_usa_decompressed_sha1':trace.ROM_SHA1,
      'original_function_sha256':FUN_SHA256,
      'compiled_guest_length':len(code),'candidate_native_exact':len(code)==1808 and code==rom[0x69ECE4:0x69F3F4],
      'cases':[]}
    for mode,label,rows,layout in cases():
        org=run(rom,None,mode,rows,layout)
        cand=run(rom,code,mode,rows,layout)
        row=summarize_case(f'base_mode{mode}_{label}',org,cand)
        report['cases'].append(row)
        print(row['case'],'OK',flush=True)
    for mode,label,rows,layout in geometry_cases():
        org=run(rom,None,mode,rows,layout)
        cand=run(rom,code,mode,rows,layout)
        row=summarize_case(f'extended_mode{mode}_{label}',org,cand)
        report['cases'].append(row)
    for mode in (0,1,2,3):
        for offset in (0,8,64,512,1024,2048):
            kind='pagemap';layout=(5,4,64,64,[0]*20)
            org=run(rom,None,mode,layout=layout,alias=(kind,offset))
            cand=run(rom,code,mode,layout=layout,alias=(kind,offset))
            expected='MemoryError' if mode in (1,2) and offset!=2048 else None
            row=summarize_case(f'alias_{kind}_mode{mode}_offset{offset}',org,cand,expected)
            report['cases'].append(row)
    for kind,modes in (('tilemap',(0,)),('texdesc',(1,2))):
        for mode in modes:
            for offset in (0,8,64,512,1024):
                org=run(rom,None,mode,alias=(kind,offset))
                cand=run(rom,code,mode,alias=(kind,offset))
                row=summarize_case(f'alias_{kind}_mode{mode}_offset{offset}',org,cand)
                report['cases'].append(row)
    for name,off in (('width_zero',0x20),('height_zero',0x22),('columns_zero',0x1c),('rows_zero',0x1e)):
        org=run(rom,None,2,zero_dim=off)
        cand=run(rom,code,2,zero_dim=off)
        if org['status']!='ArithmeticError' or cand['status']!='ArithmeticError':raise AssertionError(f'Guard test {name} failed')
        report['cases'].append({'case':'guard_'+name,'original_status':org['status'],'compiled_status':cand['status'],
                              'original_trap_pc':hex(org['pc']),'compiled_trap_pc':hex(cand['pc']),
                              'both_trap':True,'excluded_from_pass_count':True})
    counted=[r for r in report['cases'] if r.get('original_status')=='OK']
    report['summary']={'attempts':len(report['cases']),
         'completed_memory_cases':len(counted),
         'truncated_alias_cases_excluded':sum(r.get('original_status')=='MemoryError' for r in report['cases']),
         'division_guards':sum(r.get('both_trap',False) for r in report['cases']),
         'total_external_reads_each':sum(r['original_external_reads'] for r in counted),
         'total_external_stores_each':sum(r['original_external_writes'] for r in counted),
         'total_gfx_commands_each':sum(r['gfx_commands'] for r in counted),
         'all_completed_reads_equal':all(r['read_order_equal'] for r in counted),
         'all_completed_writes_equal':all(r['write_order_equal'] for r in counted),
         'all_completed_gfx_equal':all(r['gfx_equal'] for r in counted),
         'source_native_exact':report['candidate_native_exact'],'matching_c_promoted':False}
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary'],indent=2))

if __name__=='__main__':main()
