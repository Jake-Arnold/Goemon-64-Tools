typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D31F0_5FE5D0(s32, M2C_UNK);
M2C_UNK func_801EF8C8_61ACA8();                     /* static */
s32 func_801F732C_62270C(s32);                      /* static */

void func_801EF888_61AC68(s32 arg0, M2C_UNK arg1) {
    func_801D31F0_5FE5D0(arg0, 0x42200000);
    if (func_801F732C_62270C(arg0) != 0) {
        func_8003521C_35E1C(func_801EF8C8_61ACA8);
    }
}
