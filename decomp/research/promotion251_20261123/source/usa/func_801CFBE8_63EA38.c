typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern f64 D_801EEEC8_65DD18;

void func_801CFBE8_63EA38(void *arg0, M2C_UNK arg1) {
    s32 temp_f16;

    temp_f16 = (s32) ((f64) M2C_FIELD(arg0, s32 *, 0xB4) + D_801EEEC8_65DD18);
    if (temp_f16 >= 0x6D60) {
        M2C_FIELD(arg0, s8 *, 0x9E) = 1;
    }
    M2C_FIELD(arg0, s32 *, 0xB4) = temp_f16;
}
