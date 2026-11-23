typedef unsigned char u8;
typedef unsigned short u16;
typedef float f32;
extern f32 D_8020B318_5C7228;
extern void func_801DD830_599740(void *,int);
#define P(obj,o) (*(void **)((u8 *)(obj)+(o)))
#define F(obj,o) (*(f32 *)((u8 *)(obj)+(o)))
#define B(obj,o) (*(u8 *)((u8 *)(obj)+(o)))
#define H(obj,o) (*(u16 *)((u8 *)(obj)+(o)))
void func_801E2220_59E130(void *arg0) {
 F(arg0,0xA4)=D_8020B318_5C7228;
 F(arg0,0x6C)=0.0f;
 H(P(arg0,0x5C),0x30)=0;
 B(P(arg0,0x5C),0x2E)=0;
 func_801DD830_599740(arg0,1);
}
