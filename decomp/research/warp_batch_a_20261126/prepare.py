from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
rows=[]
def blob(s):
 b=s.encode();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def add(r,n,z,nrel,p,neg,sha,negsha=None,pr=276):
 assert blob(p)==sha,(n,blob(p),sha)
 if negsha: assert blob(neg)==negsha,(n,blob(neg),negsha)
 d=ROOT/'sources'/n;d.mkdir(parents=True,exist_ok=True)
 for k,s in [('candidate',p),('negative',neg)]: (d/(k+'.c')).write_text(s)
 rows.append(dict(region=r,name=n,original_bytes=z,relocation_count=nrel,source=f'sources/{n}/candidate.c',negative_source=f'sources/{n}/negative.c',source_git_blob_sha1=sha,negative_git_blob_sha1=blob(neg),negative_provenance='research PR' if negsha else 'fresh changed-source control',research_pr=pr))
for r,init,wrap,alloc,primary,final,shas in [
 ('usa','func_800357BC_363BC','func_800358E8_364E8','func_80034CBC_358BC','func_80035964_36564','func_80034D24_35924',['4de53378b2847398db168ae2b821fac20ba7a610','a990e71dfa50fa8e160e75e4956dfb28d1dcae29','8b40425a602d033128ff42d557cd64e0e6927c75','6774d2f7e421869d441557da33329ea5b2ea546a']),
 ('japan_0','func_8003542C_3602C','func_80035558_36158','func_8003492C_3552C','func_800355D4_361D4','func_80034994_35594',['600f3d36d54e09a82b8ee8c3c161aa25dcf7c944','cc29237d39733ff9bfbadb94aa86570dc7717187','4460365577eca947a335ac63c492dcafa6911544','f2453164f582fdb4131b962c1332146a56045dae'])]:
 p=f'''typedef unsigned short u16;
typedef void *Task;
extern Task {alloc}(Task, void *, int, u16);
extern Task {primary}(Task, void *, void *, float, float, float, u16, u16, u16, float, float, float, u16, u16);
Task {init}(Task a, void *b, void *c, void *d, float x, float y, float z, u16 r, u16 s, u16 t, float i, float j, float k, u16 m, u16 n) {{
    Task p = {alloc}(a, b, 2, m);
    {primary}(p, c, d, x, y, z, r, s, t, i, j, k, m, n);
    return p;
}}
''';add(r,init,152,2,p,p.replace('unsigned short','signed short',1),*shas[:2])
 p=f'''typedef unsigned short u16;
typedef void *Task;
extern Task {init}(Task, void *, void *, void *, float, float, float, u16, u16, u16, float, float, float, u16, u16);
extern Task {final}(Task);
Task {wrap}(Task a, void *b, void *c, void *d, float x, float y, float z, u16 r, u16 s, u16 t, float i, float j, float k, u16 m, u16 n) {{
    return {final}({init}(a, b, c, d, x, y, z, r, s, t, i, j, k, m, n));
}}
''';add(r,wrap,124,2,p,p.replace('unsigned short','signed short',1),*shas[2:])
for r,n,literal,cb,reg,sha,negsha in [
 ('usa','func_802151E0_5D06B0','D_8023A234_5F5704','func_80215230_5D0700','func_8003521C_35E1C','b8bf47b26a39f4d1b4ca6e38b70d9a627b609cb6','625937e5ee7dd8d1ac4d5e267a73d16da1a0ee00'),
 ('japan_0','func_80219F70_5D5500','D_8023EF44_5FA4D4','func_80219FC0_5D5550','func_80034E8C_35A8C','71baa77a189d6e3519ce832223823360a31af613','58da209ac6b87114f42f9982359b74269f18a6b3')]:
 p=f'''typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {{ u8 pad[0x5e]; u16 id; u32 a,b; }} Task;
typedef struct {{ u8 pad[0x1c]; float x,y,z; }} Object;
extern float {literal};
extern void {cb}(void);
extern void {reg}(void (*)(void));
void {n}(Task *t,Object *o) {{
    float f={literal};
    t->id=0x7e;
    o->x=f;
    o->y=f;
    o->z=f;
    t->a=0x20;
    t->b=2;
    {reg}({cb});
}}
''';add(r,n,80,5,p,p.replace('0x7e','0x7f'),sha,negsha,279)
for r,n,literal,cb,sha,negsha in [
 ('usa','func_80216E1C_5D22EC','D_8023A510_5F59E0','func_80216CE0_5D21B0','7295d3b81cd63d3588e2dfe17552fc4f6b53033f','8cc480fb14569778ab14b6bbd96b481bbf0feda9'),
 ('japan_0','func_8021BB8C_5D711C','D_8023F220_5FA7B0','func_8021BA50_5D6FE0','bb3c19a8685d74c618e136e311e197e5c382e2a6','5b6aaa85ea2a533001e2032a8dc2566b4a55405d')]:
 p=f'''typedef unsigned char u8;
typedef struct {{u8 pad[0x1c]; float x,y,z;}} Obj;
typedef struct {{u8 pad[0x18]; Obj *child;}} Task;
extern float {literal};
extern void {cb}(Task *, Obj *, int);
void {n}(Task *task,int kind) {{
    Obj *obj;
    float value;
    value={literal};
    obj=task->child;
    obj->x=value;
    obj->y=value;
    obj->z=value;
    {cb}(task,obj,kind);
}}
''';add(r,n,56,3,p,p.replace('obj->z=value','obj->z=0.0f'),sha,negsha,280)
for r,n,sha,negsha in [('usa','func_8021617C_5D164C','84236ab3223ba2e65ef5d8cfac5c5f0b6742a14d','0ad8f071b12aaadb348f260c45231d4f09da509a'),('japan_0','func_8021AEF4_5D6484','1bdf9d7368b4c7671cb86e5ef00d05c779cad12a','a5f9af5534ed6ebabe0a186e48753cb8e64fefe2')]:
 p='''typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {
    u8 pad0[4];
    u8 field4,field5,pad6[2];
    union {u32 word;struct {u32 top:3;u32 rest:2;u32 enable:1;u32 remain:7;u32 mode:4;u32 tail:15;} bits;struct {u8 flags,pad[3];} bytes;} p;
    u8 padc[4];
    u8 field10,pad11[0xB];
    u16 field1c,pad1e;
    u16 field20,pad22;
    u8 pad24[8];
    float x,y;
} Obj;
void NAME(Obj *o,u16 a,u16 b) {
    o->field4=1;
    o->p.bits.enable=1;
    o->p.bits.top=2;
    o->x=(float)(u16)a;
    o->y=(float)(u16)b;
    o->field5=10;
    o->field1c=16;
    o->field20=16;
    o->p.bits.mode=6;
    o->field10=0;
}
'''.replace('NAME',n);add(r,n,172,0,p,p.replace('    o->field4=1;\n    o->p.bits.enable=1;','    o->p.bits.enable=1;\n    o->field4=1;'),sha,negsha,280)
for r,n,literal,data,alloc,cb,sha,negsha in [('usa','func_80216E54_5D2324','D_8023A514_5F59E4','D_8006D920_6E520','func_80035EEC_36AEC','func_80216CE0_5D21B0','aafb2266132d962bd7aca92a91086fb0756188a2','72355e93f34552963c457ff4d908cace9d5da198'),('japan_0','func_8021BBC4_5D7154','D_8023F224_5FA7B4','D_80073400_74000','func_80035B5C_3675C','func_8021BA50_5D6FE0','818e6f2623de0f0440c2132e245ee8a1c6568bae','d8bc104c572017e3c2bcf625be08fab773e4362a')]:
 p=f'''typedef unsigned char u8;
typedef unsigned int u32;
typedef struct {{u8 pad[0x1c];float x,y,z;u8 pad2[8];u32 field30;}} Obj;
extern float {literal};
extern u8 {data}[];
extern Obj *{alloc}(void *,int,int);
extern void {cb}(void *,Obj *,int);
Obj *{n}(void *t,int arg){{
    Obj *o={alloc}(t,2,1);
    if(o!=0){{
        if(o!=0){{
            float f={literal};
            o->field30=(u32){data}|0x40000000;
            o->x=f;
            o->y=f;
            o->z=f;
            {cb}(t,o,arg);
            return o;
        }}
    }}
    return 0;
}}
''';add(r,n,124,6,p,p.replace('        if(o!=0){','        {'),sha,negsha,280)
(ROOT/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
print('authenticated',len(rows),'source/control pairs')
# Combined original research source is authenticated before deriving standalone sources.
for r,primary,secondary,system,cb,tailsha in [('usa','func_80035964_36564','func_80035A5C_3665C','D_8015C5C8_15D1C8','func_80014218_14E18','5864cdee00ed6bd3ff8e6e57267606411c83c851'),('japan_0','func_800355D4_361D4','func_800356CC_362CC','g_system_ptr','func_80013DA8_149A8','0fc031c512e15edf1d697003941f753908fe88e4')]:
 header=f'''typedef unsigned short u16;
typedef unsigned char u8;
typedef struct Object {{
    u8 pad0[8];
    float x,y,z;
    u16 r,s,t,pad1;
    float i,j,k,other;
    void *b,*c;
    u16 m; u8 pad2[6]; u16 n; u8 pad3[6];
    u16 field44; u8 pad4[6]; u16 field4c; u8 pad5[6];
    u16 field54; u8 pad6[6]; u16 field5c; u8 pad7[6];
    u8 field64,field65,pad8[2]; float field68,field6c,field70;
    unsigned field74,field78; u8 field7c,pad9; u16 field7e;
}} Object;
typedef struct Task {{ u8 pad[0x1c]; Object *object; }} Task;
extern u8 *{system};
extern u8 D_C2D90[];
extern void {cb}(Object *);
'''
 def body(name,mode):
  value='mode' if mode else f'*(u16 *)({system}+(unsigned int)D_C2D90)'
  args='u16 m,u16 mode,u16 n' if mode else 'u16 m,u16 n'
  return f'''Task *{name}(Task *a, void *b, void *c, float x,float y,float z,u16 r,u16 s,u16 t,float i,float j,float k,{args}) {{
    Object *o;
    if (a != 0) {{
        o = a->object;
        if (o != 0) {{
            o->b=b;
            o->c=c;
            o->x=x;
            o->y=y;
            o->z=z;
            o->r=r;
            o->s=s;
            o->t=t;
            o->i=i;
            o->j=j;
            o->k=k;
            o->m=m;
            o->n=n;
            o->field44={value};
            o->field4c=0;
            o->field54=0;
            o->field5c=0;
            {cb}(o);
            o->field64=0;
            o->field65=0;
            o->field74=0;
            o->field78=0;
            o->field7c=0;
            o->field7e=0;
            o->other=0.0f;
            o->field68=0.0f;
            o->field6c=0.0f;
            o->field70=0.0f;
        }}
    }}
    return a;
}}
'''
 combined=header+body(primary,False)+body(secondary,True); assert blob(combined)==tailsha,(r,blob(combined),tailsha)
 for n,mode,z,rels in [(primary,False,248,5),(secondary,True,232,1)]:
  p=header+body(n,mode);add(r,n,z,rels,p,p.replace('o->field4c=0','o->field4c=1'),blob(p));rows[-1]['combined_research_git_blob_sha1']=tailsha;rows[-1]['source_provenance']='standalone function extracted from authenticated combined research source'
for r,n,offset,sysp,system,arr1,arr2,call,sh in [('usa','func_80037548_38148','0xAE04','D_8015C5C8_15D1C8','D_800BCCC0_BD8C0','D_8015C830_15D430','D_8015C840_15D440','func_80003728_4328','bf0290237bc86f3363e1e196bd3c7e5183b3d773'),('japan_0','func_800371B8_37DB8','0x3AE04','g_system_ptr','g_system','D_80162020_162C20','D_80162030_162C30','func_8000364C_424C','e151856f95325976ad294b2883e71b142b1d67c9')]:
 p=f'''typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {{ u8 a[0x2DE4]; u8 state; u8 b[0xF]; u16 index; }} Partial;
typedef struct {{ u8 a[{offset}]; u32 value; u8 b[0x1D8]; u16 scene,mode,x,y; short z; u16 heading; }} Tail;
extern u8 *{sysp};
extern Tail {system};
extern u32 {arr1}[], {arr2}[];
extern u8 D_3AFE0[];
extern void {call}(int);
void {n}(void) {{
    u8 *system;
    Partial *p;
    int one=1;
    {call}(12);
    system={sysp};
    p=(Partial *)(system+0x38000);
    if(p->state==4) {{
        {arr1}[p->index]=one;
        *(u16 *)(system+(unsigned int)D_3AFE0)=p->index+0x221;
    }} else {{
        {arr2}[p->index]=one;
        switch(p->index) {{
        case 0:
            break;
        case 1:
            {system}.scene=0x132;
            {system}.mode=0;
            {system}.x=0x6C4;
            {system}.y=0x1B2;
            {system}.z=5;
            {system}.heading=0x200;
            break;
        case 2:
            {system}.value=0x49;
            {system}.scene=0x14D;
            {system}.mode=0;
            {system}.x=0xE1;
            {system}.y=0x202;
            {system}.z=-0x1F3;
            {system}.heading=0x200;
            break;
        case 3:
            break;
        }}
    }}
}}
''';add(r,n,308,None,p,p.replace('int one=1','int one=2'),sh)
p='''typedef unsigned char u8;
typedef unsigned short u16;
typedef struct { u8 a[0xADF2]; u16 current; u8 b[8]; u16 last; } Sys;
extern Sys D_800BCCC0_BD8C0;
int func_8003767C_3827C(void) {
    if (D_800BCCC0_BD8C0.last == D_800BCCC0_BD8C0.current) return 1;
    return 0;
}
''';add('usa','func_8003767C_3827C',52,None,p,p.replace('return 1','return 2'),'e1415c691b807c7d38f330ab3ad1afe6057af16c')
assert len(rows)==19 and sum(x['original_bytes'] for x in rows)==3044
(ROOT/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n');print('authenticated all',len(rows),'source/control pairs')
