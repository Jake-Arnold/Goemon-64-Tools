#include "common.h"
extern f32 sqrtf(f32);
#pragma intrinsic(sqrtf)
void func_801E32D4_59F1E4(void *, f32, f32, f32);
extern f32 D_8020B350_5C7260;
extern f32 D_8020B35C_5C726C;
extern f32 D_8020B360_5C7270;
extern f32 D_8020B364_5C7274;
void func_801E31A8_59F0B8(void *arg0) {
    f32 f = D_8020B350_5C7260;
    func_801E32D4_59F1E4(arg0,f,f,f);
}
void func_801E3244_59F154(void *arg0) {
    f32 f = D_8020B35C_5C726C;
    func_801E32D4_59F1E4(arg0,f,f,f);
}
void func_801E3278_59F188(void *arg0) {
    f32 root = sqrtf(D_8020B360_5C7270); f32 f; f = (120.0f - D_8020B364_5C7274 * root) / 40.0f;
    func_801E32D4_59F1E4(arg0,f,f,f);
}
extern void func_801E3834_59F744(void *, u32);
extern void func_801DD830_599740(void *, s32);
extern void *func_801DB494_5973A4(void *, void *, s32, s32, f32);
extern void *D_8015CCC0_15D8C0;
#define F(o,offset) (*(f32*)((u8*)(o)+(offset)))
#define P(o,offset) (*(void **)((u8*)(o)+(offset)))
#define B(o,offset) (*(u8*)((u8*)(o)+(offset)))
#define H(o,offset) (*(u16*)((u8*)(o)+(offset)))
void func_801E28D8_59E7E8(void *arg0, u8 arg1){func_801E3834_59F744(arg0,arg1);F(arg0,0xE4)=0.0f;F(arg0,0xE8)=1.0f;}
void func_801E2B54_59EA64(void *arg0){func_801DD830_599740(arg0,4); P(P(arg0,0x5C),0x88)=func_801DB494_5973A4(arg0,D_8015CCC0_15D8C0,0x196,0x80,115.0f);}
