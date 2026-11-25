typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000DD58_E958(M2C_UNK);                    /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
f32 func_801D2F40_5FE320(M2C_UNK, M2C_UNK);         /* extern */
M2C_UNK func_801F80F0_6234D0(s32, s32);             /* extern */
extern M2C_UNK func_801F3634_61EA14;

void func_801F3A68_61EE48(s32 arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    if (func_801D2F40_5FE320(arg1, 0x41F00000) == 0.0f) {
        func_801F80F0_6234D0(arg0, func_8000DD58_E958(5) & 0xFF);
        func_8003521C_35E1C(&func_801F3634_61EA14);
    }
}
