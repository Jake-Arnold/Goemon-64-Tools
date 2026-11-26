typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_800115F8_121F8(void *, s32, s32);
void func_80011610_12210(void *, void *);
s32 func_800119D4_125D4(s8 *, M2C_UNK);
s32 func_80034E08_35A08(s32, M2C_UNK *, M2C_UNK);
extern s32 func_801D0A30_6638E0;

s32 func_801D0B64_663A14(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 temp_v0;

    temp_v0 = func_80034E08_35A08(arg0, &func_801D0A30_6638E0, 0);
    if (temp_v0 == 0) {
        return 0;
    }
    func_80011610_12210((void *) temp_v0, (void *) arg0);
    func_800115F8_121F8((void *) temp_v0, arg1, arg2);
    func_800119D4_125D4((s8 *) temp_v0, arg3);
    return temp_v0;
}
