typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { u8 pad_0[12]; f32 f_C; u8 pad_10[16]; f32 f_20; } RecoveredFields_arg1;
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_8003D310_3DF10(M2C_UNK);               /* extern */
M2C_UNK func_801D326C_5FE64C(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D6508_6018E8(void *, M2C_UNK);      /* extern */
f32 func_801F7168_622548();                         /* extern */
M2C_UNK func_801F74E4_6228C4(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801EF704_61AAE4;

void func_801EF630_61AA10(void *arg0, void *arg1) {
    f32 sp1C;

    sp1C = func_801F7168_622548() - (200.0f * ((RecoveredFields_arg1 *)arg1)->f_20);
    func_801D326C_5FE64C(arg0, 0x42200000);
    func_801D6508_6018E8(arg0, 0xBDCCCCCD);
    if ((M2C_FIELD(arg0, f32 *, 0x74) <= 0.0f) && (((RecoveredFields_arg1 *)arg1)->f_C <= sp1C)) {
        M2C_FIELD(D_8020EED0_63A2B0, s8 *, 0x2C1) = 4;
        func_8003D310_3DF10(0x29A);
        func_801F74E4_6228C4(arg0, 0x3F333333, 0x3F000000, 0x3E99999A);
        func_8003521C_35E1C(&func_801EF704_61AAE4);
    }
}
