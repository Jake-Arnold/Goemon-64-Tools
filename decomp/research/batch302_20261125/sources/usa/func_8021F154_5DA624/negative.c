typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_80003E10_4A10(u16);                        /* extern */
f32 func_80003EA0_4AA0(u16);                        /* extern */

void func_8021F154_5DA624(void *arg0, f32 arg1, u16 arg2, u16 arg3) {
    volatile int negative_control = 1;

    f32 sp1C;

    sp1C = func_80003EA0_4AA0(arg2);
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) (func_80003E10_4A10(arg3) * sp1C * arg1);
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) (-func_80003E10_4A10(arg2) * arg1);
    sp1C = func_80003EA0_4AA0(arg2);
    M2C_FIELD(arg0, f32 *, 0x80) = (f32) (func_80003EA0_4AA0(arg3) * sp1C * arg1);
}
