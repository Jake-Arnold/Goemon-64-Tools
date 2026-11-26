from pathlib import Path
from replay import META
root=Path(__file__).parent/'sources'
for r,rows in META.items():
 for i,(n,z,owner,k,call1,call2,indirect,cb,register) in enumerate(rows):
  out=root/n;out.mkdir(parents=True,exist_ok=True)
  header='typedef unsigned char u8;\ntypedef unsigned short u16;\ntypedef unsigned int u32;\ntypedef struct { u8 pad[0x1c]; float x,y,z; } Obj;\n'
  header+='typedef struct { u8 pad[0x5e]; u16 id; u32 a,b; u8 pad68[0x4c]; u32 b4; } Task;\n'
  header+=f'extern float {k};\nextern void {cb}(void);\nextern void {register}(void (*)(void));\n'
  if i<2:
   header+=f'extern void {call1}(Task *);\nextern void {call2}(Task *,int,float,int);\nextern char {indirect};\n'
   pre=f'    {call1}(t);\n    {call2}(t,0,0.33333334f,1);\n'
   post=f'    ((void (*)(Task *,int,int))&{indirect})(t,10,0);\n'+('    t->b4=0;\n' if i==0 else '')+f'    {register}({cb});\n'
  else:
   header+=f'extern void {call1}(Task *,int);\n'
   pre=f'    t->id=0x7e;\n    {call1}(t,8);\n'
   post=f'    t->a=0x20;\n    t->b=2;\n    {register}({cb});\n'
  sig=f'void {n}(Task *t,Obj *o) {{\n'
  def save(name,body,decl=''): (out/(name+'.c')).write_text(header+sig+decl+pre+body+post+'}\n')
  save('00_named_chain',f'    o->x=o->y=o->z={k};\n')
  save('01_named_local',f'    f={k};\n    o->x=o->y=o->z=f;\n','    float f;\n')
  save('02_literal_chain',f'    o->x=o->y=o->z={"0.1f" if i<2 else "0.2f"};\n')
  save('03_literal_local',f'    f={"0.1f" if i<2 else "0.2f"};\n    o->x=o->y=o->z=f;\n','    float f;\n')
