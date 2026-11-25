typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80038838_39438(s32);
void func_801D8604_603084(void *, void *);
void func_801D8BF0_603670(void *, s32, s32, s32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern M2C_UNK D_802107C4_63B244;
extern M2C_UNK D_802108B8_63B338;
extern M2C_UNK func_801EDBB8_618638;

void func_801EDA98_618518(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg0, s32 *, 0xB0) = 0;
    M2C_FIELD(arg0, f32 *, 0x74) = 7.0f;
    func_801D8604_603084(arg1, &D_802108B8_63B338);
    func_801D8BF0_603670(arg1, (s32) &D_802107C4_63B244, 0, 1);
    func_80038838_39438(0x34E);
    M2C_FIELD(arg0, s32 *, 0xE8) = (s32) (M2C_FIELD(arg0, s32 *, 0xE8) + 1);
    func_80034E8C_35A8C(&func_801EDBB8_618638);
}
