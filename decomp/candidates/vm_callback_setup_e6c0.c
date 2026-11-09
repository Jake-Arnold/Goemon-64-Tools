/* Research only. USA func_8003E6C0_3F2C0 (348 original MIPS bytes). */
typedef unsigned int u32;
typedef signed int s32;
typedef signed short s16;
typedef unsigned char u8;
typedef struct {
  u8 pad00[0x32];s16 x; s16 y;
  u8 pad36[0x1A];s32 addx; s32 addy;
  u8 pad58[0x16];s16 offx;
  u8 pad70[4];s16 offy;
} VmWindow;
typedef struct {u32 x,y,prev,next,script;} VmChoice;
extern void *D_801C78D0_1C84D0;
extern s32 D_801C7754_1C8354;
extern VmWindow *D_80167C48_168848[];
#ifndef GOEMON_VM_E6C0_HOST_TEST
extern VmChoice D_801C7808_1C8408[];
#else
extern VmChoice *vm_e6c0_choice_base;
#define D_801C7808_1C8408 vm_e6c0_choice_base
#endif
extern u8 D_801C77F4_1C83F4[];
extern u8 D_801C781C_1C841C[];
extern s32 D_801C77E0_1C83E0;
extern s32 func_80034B24_35724(void *,s32);
extern s32 func_8003DE48_3EA48(s32);
extern void func_8003EB34_3F734(s32,s32);
extern void func_8003E9E8_3F5E8(VmChoice *);
#ifdef GOEMON_VM_E6C0_HOST_TEST
#include <stdint.h>
#define VM_E6C0_PTR(x) ((u32)(uintptr_t)(x))
#else
#define VM_E6C0_PTR(x) ((u32)(x))
#endif
u32 *func_8003E6C0_3F2C0(u32 *script) {
  VmWindow *w;
  s32 n=0;
  if(D_801C78D0_1C84D0 != 0) func_80034B24_35724(D_801C78D0_1C84D0,0);
  w=D_80167C48_168848[D_801C7754_1C8354];
  while (*script != 0x8012) {
    VmChoice *p=&D_801C7808_1C8408[n];
    p->x=(u32)(s32)w->x + (u32)(s32)w->offx + (u32)w->addx;
    p->y=(u32)(s32)w->y + (u32)(s32)w->offy + (u32)w->addy;
    p->prev=VM_E6C0_PTR(D_801C77F4_1C83F4+20*n);
    p->next=VM_E6C0_PTR(D_801C781C_1C841C+20*n);
    { s32 result=func_8003DE48_3EA48((s32)script[1]);
      func_8003EB34_3F734(D_801C7754_1C8354,result); }
    p->script=VM_E6C0_PTR(script+2);
    ++n;
    script+=4;
  }
  D_801C7808_1C8408[0].prev=0;
  *(u32 *)((u8 *)D_801C7808_1C8408 + n*20-8)=0;
  func_8003E9E8_3F5E8(D_801C7808_1C8408);
  D_801C77E0_1C83E0=2;
  return script;
}
