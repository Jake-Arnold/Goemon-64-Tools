typedef unsigned char u8;
typedef unsigned short u16;
typedef float f32;
extern f32 sqrtf(f32);
#pragma intrinsic(sqrtf)
extern f32 D_8020B30C_5C721C;
extern f32 D_8020B310_5C7220;
extern f32 D_8020B314_5C7224;
extern int func_801E7DE8_5A3CF8(void *);
extern void func_801DD830_599740(void *,int);
extern void func_80038BC8_397C8(int);
extern void func_801DD6E0_5995F0(void *,int);
#define P(obj,o) (*(void **)((u8 *)(obj)+(o)))
#define F(obj,o) (*(f32 *)((u8 *)(obj)+(o)))
#define B(obj,o) (*(u8 *)((u8 *)(obj)+(o)))
#define H(obj,o) (*(u16 *)((u8 *)(obj)+(o)))
void func_801E2180_59E090(void *arg0) {
  f32 chosen;
  if (func_801E7DE8_5A3CF8(arg0)) chosen=D_8020B30C_5C721C;
  else chosen=D_8020B310_5C7220;
  F(arg0,0xA4)=sqrtf(chosen)+D_8020B314_5C7224;
  F(arg0,0x6C)=0.0f;
  H(P(arg0,0x5C),0x30)=0;
  B(P(arg0,0x5C),0x2E)=0;
  func_801DD830_599740(arg0,1);
  if(func_801E7DE8_5A3CF8(arg0))func_80038BC8_397C8(0x2B5);
  else func_801DD6E0_5995F0(arg0,0x21);
}
