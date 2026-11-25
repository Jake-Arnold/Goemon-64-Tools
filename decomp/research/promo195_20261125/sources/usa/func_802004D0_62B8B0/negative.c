typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern void *D_8020EED0_63A2B0;
extern void *D_8020EF40_63A320;

void func_802004D0_62B8B0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        M2C_FIELD(D_8020EF40_63A320, s8 *, 5) = 1;
    }
    M2C_FIELD(D_8020EED0_63A2B0, s8 *, 0x2C1) = 2;
}
