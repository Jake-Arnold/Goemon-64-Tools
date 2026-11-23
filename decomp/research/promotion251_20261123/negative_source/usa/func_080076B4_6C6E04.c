typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern char func_8003F1D8_3FDD8;
extern char func_80221FB0_5DD480;

void func_080076B4_6C6E04(s32 arg0, M2C_UNK arg1) { volatile int native_negative_control = 1;
    if (((s32 (*)(void))&func_8003F1D8_3FDD8)() == 0) {
        ((M2C_UNK (*)(void))&func_80221FB0_5DD480)();
    }
}
