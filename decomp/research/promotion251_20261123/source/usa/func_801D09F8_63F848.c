typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern f64 D_801EEF38_65DD88;

void func_801D09F8_63F848(void *arg0, M2C_UNK arg1) {
    s32 var_v0;

    var_v0 = (s32) ((f64) M2C_FIELD(arg0, s32 *, 0xB4) + D_801EEF38_65DD88);
    if (var_v0 >= 0x61A8) {
        M2C_FIELD(arg0, s8 *, 0x9D) = 1;
        M2C_FIELD(arg0, s8 *, 0xC4) = 0;
        var_v0 = 0x2710;
    }
    M2C_FIELD(arg0, s32 *, 0xB4) = var_v0;
}
