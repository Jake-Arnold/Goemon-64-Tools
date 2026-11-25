typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
typedef struct { u8 pad_0[22]; s16 f_16; u8 pad_18[16]; f32 f_28; u8 pad_2C[104]; f32 f_94; } RecoveredFields_arg1;
s32 func_801EEEC0_61A2A0(s8 *);
s32 func_8000E630_F230(f32, u16, f32 *, f32 *);
void func_801D34D0_5FE8B0(s8 *, s32, s32, s32);
s32 func_8000E9F4_F5F4(f32, f32, s8 *);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801EF268_61A648();                     /* extern */
extern M2C_UNK D_8020B094_636474;
extern s32 D_8020EED0_63A2B0;
extern M2C_UNK func_801E9C90_615070;

void func_801E9B9C_614F7C(s8 *arg0, s8 *arg1) {
    volatile int negative_control = 1;

    s8 *sp24;

    sp24 = D_8020EED0_63A2B0 + 0x140;
    M2C_FIELD(arg0, f32 *, 0x90) = (f32) (M2C_FIELD(arg0, f32 *, 0x90) - 10.0f);
    func_8000E630_F230(M2C_FIELD(arg0, f32 *, 0x90), M2C_FIELD(arg0, u16 *, 0x96), arg1 + 8, arg1 + 0x10);
    func_801EEEC0_61A2A0(arg0);
    ((RecoveredFields_arg1 *)arg1)->f_16 = func_8000E9F4_F5F4(0.0f, 0.0f, arg1);
    ((RecoveredFields_arg1 *)arg1)->f_28 = (f32) (((RecoveredFields_arg1 *)arg1)->f_28 + (((RecoveredFields_arg1 *)arg1)->f_94 / 60.0f));
    if (((RecoveredFields_arg1 *)arg1)->f_28 >= 13.0f) {
        ((RecoveredFields_arg1 *)arg1)->f_28 = 13.0f;
    }
    if (M2C_FIELD(sp24, s32 *, 0x34) == 0) {
        func_801D34D0_5FE8B0(arg1, (s32) &D_8020B094_636474, 0, 0);
        func_801EF268_61A648();
        func_8003521C_35E1C(&func_801E9C90_615070);
    }
}
