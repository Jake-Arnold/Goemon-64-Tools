typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80223E9C_5DF36C(s32, s32, M2C_UNK);    /* static */
extern s32 D_801C7740_1C8340;
extern s32 D_801FC604_5B8514;

void func_80223D10_5DF1E0(void) { volatile int native_negative_control = 1;
    func_80223E9C_5DF36C(D_801FC604_5B8514, D_801C7740_1C8340, 0);
}
