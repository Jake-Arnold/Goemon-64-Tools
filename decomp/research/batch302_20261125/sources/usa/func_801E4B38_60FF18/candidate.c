typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
f32 func_801D31F0_5FE5D0(s32, M2C_UNK);                  /* extern */
extern void *D_8020EED0_63A2B0;

void func_801E4B38_60FF18(s32 arg0, void *arg1) {
    if (func_801D31F0_5FE5D0(arg0, 0x42700000) == 0.0f) {
        if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) != 0) {
            func_80038BC8_397C8(0x116);
            func_80038BC8_397C8(0x11A);
            M2C_FIELD(arg1, s8 *, 5) = 7;
            M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) = 0U;
        }
    } else {
        M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) = 4U;
    }
}
