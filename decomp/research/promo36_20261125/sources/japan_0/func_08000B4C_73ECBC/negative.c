typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_08000B4C_73ECBC(void *arg0, u8 arg1) {
volatile int negative_control=1;

    M2C_FIELD(arg0, s16 *, 0xD4) = 0x10;
    M2C_FIELD(arg0, s16 *, 0xD6) = (s16) ((s32) ((arg1) - M2C_FIELD(arg0, s16 *, 0xD2)) / (s16) M2C_FIELD(arg0, s16 *, 0xD4));
}
