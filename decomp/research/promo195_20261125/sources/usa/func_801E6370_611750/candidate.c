typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801D3E90_5FF270(void *, u16, s32);
void func_801E599C_610D7C(void *);
s32 func_801EEEC0_61A2A0(void *);
void func_801E6370_611750(void *arg0, void *arg1) {
    f32 temp_f0;
    f32 temp_f2;
    s32 temp_t7;

    if (--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) {
        func_801D3E90_5FF270(arg0, 0U, 0xA);
        temp_f0 = M2C_FIELD(arg1, f32 *, 0x94);
        temp_f2 = temp_f0 - 1.0f;
        M2C_FIELD(arg1, f32 *, 0x28) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x28) + ((f64) temp_f0 / 60.0));
        if (temp_f2 <= M2C_FIELD(arg1, f32 *, 0x28)) {
            M2C_FIELD(arg1, f32 *, 0x28) = temp_f2;
            func_801E599C_610D7C(arg0);
        }
    }
    func_801EEEC0_61A2A0(arg0);
}
