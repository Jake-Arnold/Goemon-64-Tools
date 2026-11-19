/* Host semantic tests. 64-bit host pointer offsets are not N64 layout assertions. */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef short s16;
typedef struct { float xyz[6]; u16 unknown_18; u16 input_1A; u32 remaining[17]; } State96;
typedef struct {u8 padding[0x6C]; State96 *state;} StateOwner;
typedef struct {u8 flag;u8 pad;s16 index;float speed;u32 value;} Record;
typedef struct {u8 pad[0xC8];s16 count;s16 max; Record * volatile record;} Owner;
typedef struct {u8 padding[0x5D]; u8 type;u8 extra[2];float x,y,z;} Params;
typedef struct {u8 padding[0x5C];float a;float b;float pad1[2];float c;float pad2[2];float d;} FloatState;
typedef struct {u8 prefix[4];u8 flags;} Linked;
typedef struct {u8 prefix[0x1C];Linked *linked;} Outer;
extern void func_80012878_13478(StateOwner *,State96 *);
extern void func_80012900_13500(StateOwner *,State96 *);
extern State96 *func_80012938_13538(StateOwner *);
extern void func_800125D0_131D0(Params *,int,float,float,float);
extern void func_800125F0_131F0(Owner *,int,u32,float,s16);
extern void func_800133D4_13FD4(FloatState *,float);
extern void func_800133E0_13FE0(FloatState *,float,float,float);
extern void func_80013508_14108(Outer *);
static unsigned calls;static float a[3],b[3];static u16 flag16;
void func_800127B8_133B8(StateOwner *o,float x,float y,float z){assert(o);calls|=1;a[0]=x;a[1]=y;a[2]=z;}
void func_80012818_13418(StateOwner *o,float x,float y,float z){assert(o);calls|=2;b[0]=x;b[1]=y;b[2]=z;}
void func_80012500_13100(StateOwner *o,u16 v){assert(o);calls|=4;flag16=v;}
int main(void){
    State96 src={0},dst={0},out={0};StateOwner owner={0};owner.state=&dst;
    for(int i=0;i<6;i++)src.xyz[i]=(float)i+0.5f;
    for(int i=0;i<17;i++)src.remaining[i]=0xAB000000u+(u32)i;
    src.unknown_18=0x9911;src.input_1A=0xEF99;
    assert(sizeof(State96)==0x60);
    func_80012878_13478(&owner,&src);
    assert(calls==7&&flag16==0xEF99);
    assert(!memcmp(&src,&dst,sizeof(src)));
    for(int i=0;i<3;i++){assert(a[i]==src.xyz[i]);assert(b[i]==src.xyz[i+3]);}
    assert(func_80012938_13538(&owner)==&dst);
    func_80012900_13500(&owner,&out);assert(!memcmp(&src,&out,sizeof(out)));
    out.xyz[0]=1234.0f;assert(src.xyz[0]==dst.xyz[0]);

    Params p={0};p.type=9;p.x=1.0f;p.y=2.0f;p.z=3.0f;
    func_800125D0_131D0(&p,257,-1.25f,3.5f,127.0f);
    assert(p.type==1&&p.x==-1.25f&&p.y==3.5f&&p.z==127.0f);
    Record rec={0};Owner ow={0};ow.record=&rec;ow.count=52;ow.max=-1;
    func_800125F0_131F0(&ow,0x1234,0xFCABEF01u,1.625f,(s16)-51);
    assert(rec.flag==1&&rec.index==0x1234&&rec.speed==1.625f&&rec.value==0xFCABEF01u);
    assert(ow.count==0&&ow.max==-51);

    FloatState fs={0};fs.pad1[0]=333;fs.pad2[1]=444;
    func_800133D4_13FD4(&fs,-2.25f);func_800133E0_13FE0(&fs,1.25f,-4.5f,7.75f);
    assert(fs.a==-2.25f&&fs.b==1.25f&&fs.c==-4.5f&&fs.d==7.75f);
    assert(fs.pad1[0]==333&&fs.pad2[1]==444);
    Linked linked={0};Outer outer={0};outer.linked=&linked;linked.flags=0x15;
    func_80013508_14108(&outer);assert(linked.flags==0x95);
    func_80013508_14108(&outer);assert(linked.flags==0x95);
    puts("PASS: eight dracam original-address C functions host semantic regression");
}
