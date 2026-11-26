typedef unsigned char u8;
typedef unsigned short u16;
typedef float f32;
extern f32 sqrtf(f32);
#pragma intrinsic(sqrtf)
extern f32 D_8021017C_5CC14C;
extern f32 D_80210180_5CC150;
extern f32 D_80210184_5CC154;
extern int func_801ECF10_5A8EE0(void *);
extern void func_801E2BE0_59EBB0(void *,int);
extern void func_80038838_39438(int);
extern void func_801E2A90_59EA60(void *,int);
#define P(obj,o) (*(void **)((u8 *)(obj)+(o)))
#define F(obj,o) (*(f32 *)((u8 *)(obj)+(o)))
#define B(obj,o) (*(u8 *)((u8 *)(obj)+(o)))
#define H(obj,o) (*(u16 *)((u8 *)(obj)+(o)))
void func_801E73C8_5A3398(void *arg0) {
  f32 chosen;
  if (func_801ECF10_5A8EE0(arg0)) chosen=D_8021017C_5CC14C;
  else chosen=D_80210180_5CC150;
  F(arg0,0xA4)=sqrtf(chosen)+D_80210184_5CC154;
  F(arg0,0x6C)=0.0f;
  H(P(arg0,0x5C),0x30)=0;
  B(P(arg0,0x5C),0x2E)=0;
  func_801E2BE0_59EBB0(arg0,1);
  if(func_801ECF10_5A8EE0(arg0))func_80038838_39438(0x2B5);
  else func_801E2A90_59EA60(arg0,0x21);
}
