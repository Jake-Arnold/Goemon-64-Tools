#!/usr/bin/env python3
"""Independent ROM-anchored original-MIPS vs C-model command stream comparison.

This harness compiles the intentionally NOT-native-matched host model. It
requires the locally unpacked research kit, but no network, emulator or ROM
modification. Original ROM bytes remain local and are never exported.
"""
from __future__ import annotations
import argparse,ctypes,hashlib,json,struct,subprocess,tempfile
from pathlib import Path
from trace_original_file22_mips import run_once,FILE22_ROM,FILE22_VMA,FILE22_LEN,SAVED_DESC,prepare

class CInput(ctypes.Structure):
 _fields_=[('pages',ctypes.POINTER(ctypes.c_uint8)),('page_count',ctypes.c_size_t),('tile_ids',ctypes.POINTER(ctypes.c_uint16)),('tile_count',ctypes.c_size_t),('format_entries',ctypes.POINTER(ctypes.c_uint16)),('format_count',ctypes.c_size_t),('texture_guest_base',ctypes.c_uint32),('page_cols',ctypes.c_int16),('page_rows',ctypes.c_int16),('pixel_width',ctypes.c_int16),('pixel_height',ctypes.c_int16),('format',ctypes.c_uint8)]
class COut(ctypes.Structure):
 _fields_=[('w0',ctypes.c_uint32),('w1',ctypes.c_uint32)]
class CResult(ctypes.Structure):
 _fields_=[('tiles_drawn',ctypes.c_size_t),('texture_setup_count',ctypes.c_size_t),('commands_emitted',ctypes.c_size_t),('last_tile_id',ctypes.c_uint16)]

def compare(rom,lib,mode,rows=None,layout=None):
   trace,actual=run_once(rom,mode,rows,layout)
   memory=prepare(rom,mode,rows,layout)
   pageaddr=memory.load(SAVED_DESC+4)
   tilesaddr=memory.load(SAVED_DESC+8)
   formataddr=memory.load(SAVED_DESC+12)
   descargs=[struct.unpack('>h',memory.load(SAVED_DESC+i,2).to_bytes(2,'big'))[0] for i in (0x1c,0x1e,0x20,0x22)]
   pagecount=layout[0]*layout[1] if layout else 1
   pages=(ctypes.c_uint8*pagecount)(*(memory.load(pageaddr+i,1) for i in range(pagecount)))
   tiles=(ctypes.c_uint16*80)(*(memory.load(tilesaddr+2*i,2) for i in range(80)))
   formats=(ctypes.c_uint16*80)(*(memory.load(formataddr+2*i,2) for i in range(80)))
   setting=CInput(pages,pagecount,tiles,80,formats,80,memory.load(SAVED_DESC+16),*descargs,mode)
   result=CResult();buf=(COut*5000)()
   rc=lib.file22_tile_display_model(ctypes.byref(setting),buf,len(buf),ctypes.byref(result))
   if rc!=1:raise AssertionError(f'Model failed mode {mode}')
   expected=[(buf[i].w0,buf[i].w1) for i in range(result.commands_emitted)]
   different=[(i,expected[i] if i<len(expected) else None,actual[i] if i<len(actual) else None) for i in range(max(len(expected),len(actual))) if i>=min(len(expected),len(actual)) or expected[i]!=actual[i]]
   return {
     'mode':mode,'rows':list(rows) if rows is not None else 'original ROM',
     'layout':str(layout) if layout is not None else 'default ROM',
     'original_commands':len(actual),'c_model_commands':len(expected),
     'command_by_command_equal':not different,
     'different_command_pairs':len(different),
     'first_difference':None if not different else {'index':different[0][0],'model':different[0][1],'mips':different[0][2]},
     'original_instruction_count':trace['original_guest_instructions_executed'],
     'original_texture_setups':trace['texture_setup_count'],'original_rectangles':trace['texture_rect_count'],
     'model_texture_setups':result.texture_setup_count,'model_rectangles':result.tiles_drawn,
     'original_gfx_sha256':trace['original_gfx_wordstream_sha256'],
     'model_gfx_sha256':hashlib.sha256(b''.join(struct.pack('>II',*x) for x in expected)).hexdigest(),
   }

def main():
 a=argparse.ArgumentParser();a.add_argument('--rom',required=True,type=Path);a.add_argument('--model',required=True,type=Path);a.add_argument('--output',type=Path)
 args=a.parse_args()
 rom=args.rom.read_bytes()
 with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'model.so'
   subprocess.run(['cc','-std=c11','-O1','-shared','-fPIC','-Wall','-Wextra','-Werror',str(args.model),'-o',str(out)],check=True)
   lib=ctypes.CDLL(str(out));lib.file22_tile_display_model.argtypes=[ctypes.POINTER(CInput),ctypes.POINTER(COut),ctypes.c_size_t,ctypes.POINTER(CResult)];lib.file22_tile_display_model.restype=ctypes.c_int
   reports=[]
   layouts = [
      ('four_pages_160x128',(2,2,160,128,[0,1,2,3])),
      ('twenty_pages_64x64',(5,4,64,64,[i%4 for i in range(20)])),
   ]
   for mode in (0,1,2,3):
     reports.append(compare(rom,lib,mode,None))
     reports.append(compare(rom,lib,mode,[0,4,0,3,2,1,4,0]))
     reports.append(compare(rom,lib,mode,[0]*8))
     for label,layout in layouts:
       x=compare(rom,lib,mode,None,layout)
       x['scenario_name']=label
       reports.append(x)
   if args.output:args.output.write_text(json.dumps(reports,indent=2)+'\n')
   print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
