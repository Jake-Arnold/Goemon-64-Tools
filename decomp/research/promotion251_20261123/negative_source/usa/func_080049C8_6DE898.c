typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
M2C_UNK func_08004A10_6DE8E0();                     /* static */

void func_080049C8_6DE898(M2C_UNK arg0, M2C_UNK arg1) { volatile int native_negative_control = 1;
    ((M2C_UNK (*)(M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0x3F800000, 1);
    ((M2C_UNK (*)(M2C_UNK (*)()))&func_8003521C_35E1C)(func_08004A10_6DE8E0);
}
