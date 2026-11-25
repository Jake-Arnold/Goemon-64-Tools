typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
void func_80038838_39438(s32);
void func_801D8604_603084(void *, void *);
f32 func_801D8910_603390(void *, f32);
void func_801D8BF0_603670(void *, s32, s32, s32);
s32 func_801D9238_603CB8(void *, f32, u16);
void func_801D9620_6040A0(void *, u16, s32);
extern M2C_UNK D_802107C4_63B244;
extern M2C_UNK D_802108F0_63B370;
extern M2C_UNK func_801EBC4C_6166CC;

void func_801EBBA4_616624(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    func_801D9238_603CB8(arg0, 80.0f, 0xAU);
    func_801D9620_6040A0(arg0, 0U, 8);
    if (func_801D8910_603390(arg0, 20.0f) == 0.0f) {
        func_80038838_39438(0x235);
        func_801D8604_603084(arg1, &D_802108F0_63B370);
        func_801D8BF0_603670(arg1, (s32) &D_802107C4_63B244, 0, 0);
        func_80034E8C_35A8C((s32) &func_801EBC4C_6166CC);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x14;
    }
}
