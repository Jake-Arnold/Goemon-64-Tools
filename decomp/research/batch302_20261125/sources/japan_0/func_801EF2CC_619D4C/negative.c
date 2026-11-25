typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
typedef struct { u8 pad_0[22]; s16 f_16; u8 pad_18[16]; f32 f_28; u8 pad_2C[104]; f32 f_94; } RecoveredFields_arg1;
s32 func_801F45F0_61F070(s8 *);
s32 func_8000E3F0_EFF0(f32, u16, f32 *, f32 *);
void func_801D8BF0_603670(s8 *, s32, s32, s32);
s32 func_8000E7B4_F3B4(f32, f32, s8 *);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801F4998_61F418();                     /* extern */
extern M2C_UNK D_802107C4_63B244;
extern s32 D_80214600_63F080;
extern M2C_UNK func_801EF3C0_619E40;

void func_801EF2CC_619D4C(s8 *arg0, s8 *arg1) {
    volatile int negative_control = 1;

    s8 *sp24;

    sp24 = D_80214600_63F080 + 0x140;
    M2C_FIELD(arg0, f32 *, 0x90) = (f32) (M2C_FIELD(arg0, f32 *, 0x90) - 10.0f);
    func_8000E3F0_EFF0(M2C_FIELD(arg0, f32 *, 0x90), M2C_FIELD(arg0, u16 *, 0x96), arg1 + 8, arg1 + 0x10);
    func_801F45F0_61F070(arg0);
    ((RecoveredFields_arg1 *)arg1)->f_16 = func_8000E7B4_F3B4(0.0f, 0.0f, arg1);
    ((RecoveredFields_arg1 *)arg1)->f_28 = (f32) (((RecoveredFields_arg1 *)arg1)->f_28 + (((RecoveredFields_arg1 *)arg1)->f_94 / 60.0f));
    if (((RecoveredFields_arg1 *)arg1)->f_28 >= 13.0f) {
        ((RecoveredFields_arg1 *)arg1)->f_28 = 13.0f;
    }
    if (M2C_FIELD(sp24, s32 *, 0x34) == 0) {
        func_801D8BF0_603670(arg1, (s32) &D_802107C4_63B244, 0, 0);
        func_801F4998_61F418();
        func_80034E8C_35A8C(&func_801EF3C0_619E40);
    }
}
