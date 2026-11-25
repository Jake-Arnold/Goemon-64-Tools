typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK * func_80035A6C_3666C(void *, s16, s32);
M2C_UNK * func_800347C8_353C8(void *, s32, u16);
void func_80034CB4_358B4(s32);
extern s32 *D_80072E00_73A00;

s32 *func_80034728_35328(void *arg0, s32 arg1, u8 arg2) {
    s32 *temp_v0;

    s32 *sp1C;
    temp_v0 = func_800347C8_353C8(arg0, arg1, 0U);
    if (temp_v0 == NULL) {
        return NULL;
    }
    if (temp_v0 != NULL) {
        sp1C = temp_v0;
        if (func_80035A6C_3666C(temp_v0, 2, (s32) arg2) == NULL) {
            func_80034CB4_358B4((s32) temp_v0);
            return NULL;
        }
    }
    D_80072E00_73A00 = temp_v0;
    return temp_v0;
}
