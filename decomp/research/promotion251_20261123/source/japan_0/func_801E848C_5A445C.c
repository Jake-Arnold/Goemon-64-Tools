typedef float f32; typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32; typedef int s32;
extern f32 sqrtf(f32);
#pragma intrinsic(sqrtf)
void func_801E84E8_5A44B8(void *, f32, f32, f32);
extern f32 D_8020B350_5C7260;
extern f32 D_8020B35C_5C726C;
extern f32 D_802101CC_5CC19C;
extern f32 D_802101D0_5CC1A0;


void func_801E848C_5A445C(void *arg0) {
    f32 root = sqrtf(D_802101CC_5CC19C); f32 f; f = (120.0f - D_802101D0_5CC1A0 * root) / 40.0f;
    func_801E84E8_5A44B8(arg0,f,f,f);
}
extern void func_801E3834_59F744(void *, u32);
extern void func_801DD830_599740(void *, s32);
extern void *func_801DB494_5973A4(void *, void *, s32, s32, f32);
extern void *D_8015CCC0_15D8C0;
#define F(o,offset) (*(f32*)((u8*)(o)+(offset)))
#define P(o,offset) (*(void **)((u8*)(o)+(offset)))
#define B(o,offset) (*(u8*)((u8*)(o)+(offset)))
#define H(o,offset) (*(u16*)((u8*)(o)+(offset)))


