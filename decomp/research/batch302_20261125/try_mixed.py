"""Trial only: adapt isolated native C declarations to existing mixed units."""
import argparse, pathlib, re, json, hashlib, subprocess, shutil
from decomp.consolidated_batch_promotion import stage, opening, cross, glitch, inventory
from decomp import usa_short72_promotion as short72, native251_promotion as native
P=pathlib.Path; ROOT=P(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def text(p):
 b=p.read_bytes(); s=opening.elf_sections(b)['.text'];return b[s['offset']:s['offset']+s['size']]
def run(co,w,uv,jobs):
 w.mkdir();r='usa';bd=co/'build/usa';ld=(co/'.splat/usa/mnsg.ld').read_text();rows=json.loads((ROOT/'usa-candidates.json').read_text());rows={x['name']:x for x in rows};d={'status':'RESEARCH_ONLY','units':[]};report=w/'summary.json';save=lambda:report.write_text(json.dumps(d,indent=2)+'\n')
 for file,names in [('src/92F0.c',['func_8000A130_AD30']),('src/return_zero.c',['func_80023394_23F94','func_80023480_24080','func_800234D8_240D8','func_80023610_24210'])]:
  src=co/file;obj=bd/(file+'.o');old=src.read_text();oldobj=w/(src.stem+'-prior.o');shutil.copyfile(obj,oldobj);rec={'unit':file,'names':names,'original_source_sha256':sha(old.encode())};d['units'].append(rec);save();new=old
  for name in names:
   row=rows[name];s=(ROOT/row['source']).read_text();assert sha(s.encode())==row['source_sha256'];pattern=rf'(?m)^#pragma GLOBAL_ASM\("[^\n"]*/{name}\.s"\)';assert len(re.findall(pattern,new))==1
   body=s[s.index('\nvoid '+name+'(' if name=='func_8000A130_AD30' else '\ns32 '+name+'(')+1:];body=body.replace('M2C_UNK','s32');body=body.replace('M2C_FIELD','BATCH302_FIELD');macro='#define BATCH302_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))\n'
   if name=='func_8000A130_AD30': decl='extern void func_8000A18C_AD8C(void);\nextern s32 func_8000A228_AE28(s32 *);\nextern s32 D_8014FA54_150654;\n'
   else:
    decl='extern s32 func_80023ADC_246DC(s32);\nextern s32 D_80168E84_169A84;\n'
    if name=='func_80023394_23F94':
     decl+='extern s32 osPfsAllocateFile(s8 *, s32, s32, s32 *, s32 *, s32, s8 *);\nextern s32 D_8006D170_6DD70, D_80168A00_169600;\n';body=body.replace('osPfsAllocateFile(D_80168E84_169A84,','osPfsAllocateFile((s8 *)D_80168E84_169A84,').replace('D_80168E84_169A84 + 0x3F0','(s8 *)D_80168E84_169A84 + 0x3F0')
    elif name=='func_80023480_24080':
     decl+='extern s32 osPfsFileState(void *, s32, void *);\n';body=body.replace('osPfsFileState(D_80168E84_169A84,','osPfsFileState((void *)D_80168E84_169A84,')
    else:
     decl+='extern s32 osPfsReadWriteFile(void *, s32, s32, s32, s32, s32);\n';body=body.replace('osPfsReadWriteFile(D_80168E84_169A84,','osPfsReadWriteFile((void *)D_80168E84_169A84,')
   new=re.sub(pattern,lambda m:macro+decl+body.rstrip()+'\n#undef BATCH302_FIELD',new,count=1)
  if file=='src/92F0.c':new=new.replace('/* Original native C for func_8000A0F0_ACF0 */','void func_8000A130_AD30(void);\n/* Original native C for func_8000A0F0_ACF0 */',1)
  integrated=w/src.name;integrated.write_text(new);rec['integrated_source_sha256']=sha(new.encode());src.write_text(new);(stage.ROOT/'COMPILER_QUIRKS.md').read_bytes()
  try:
   stage.runmake(co,r,ld,[f'build/usa/{file}.o'],w/(src.stem+'-compile.log'),uv,jobs);rec['whole_unit_text_equal']=text(oldobj)==text(obj);rec['old_text_bytes']=len(text(oldobj));rec['new_text_bytes']=len(text(obj));
   if not rec['whole_unit_text_equal']:rec['first_text_difference']=next((i for i,(a,b) in enumerate(zip(text(oldobj),text(obj))) if a!=b),min(len(text(oldobj)),len(text(obj))))
  except subprocess.CalledProcessError as e:rec['error']='native mixed compile failed'
  finally:src.write_text(old);shutil.copyfile(oldobj,obj);save()
 return d
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checkout',type=P,required=True);p.add_argument('--work',type=P,required=True);p.add_argument('--uv',required=True);p.add_argument('--jobs',type=int,default=4);a=p.parse_args();print(json.dumps(run(a.checkout,a.work,a.uv,a.jobs),indent=2))
