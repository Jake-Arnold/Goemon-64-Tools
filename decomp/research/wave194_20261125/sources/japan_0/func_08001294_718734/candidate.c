typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern void *D_80201538_5BD508;

s32 func_08001294_718734(void *arg0, f32 arg1) {
    f32 temp_f0;
    f32 temp_f12;
    f32 temp_f2;
    s32 temp_t7;
    void *temp_v1;

    temp_t7 = M2C_FIELD(D_80201538_5BD508, s32 *, 0x2C) & 0x8FFFFFFE;
    temp_v1 = M2C_FIELD(arg0, void **, 0x18);
    temp_f0 = M2C_FIELD(temp_v1, f32 *, 8) - M2C_FIELD(temp_t7, f32 *, 0);
    temp_f2 = M2C_FIELD(temp_v1, f32 *, 0xC) - M2C_FIELD(temp_t7, f32 *, 4);
    temp_f12 = M2C_FIELD(temp_v1, f32 *, 0x10) - M2C_FIELD(temp_t7, f32 *, 8);
    if (((temp_f0 * temp_f0) + (temp_f2 * temp_f2) + (temp_f12 * temp_f12)) < (arg1 * arg1)) {
        return 1;
    }
    return 0;
}
