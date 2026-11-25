typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern M2C_UNK D_3AE29;
extern M2C_UNK D_3AFE0;
extern s32 D_8015C5C8_15D1C8;

void func_80037414_38014(void) {
    volatile int negative_control = 1;

    *(u8 *)((u32)&D_3AE29 + (D_8015C5C8_15D1C8)) = 0x80;
    *(u16 *)((u32)&D_3AFE0 + (D_8015C5C8_15D1C8)) = 0x221;
}
