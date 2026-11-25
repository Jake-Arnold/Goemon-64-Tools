typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034ED4_35AD4();                      /* extern */
M2C_UNK func_801D606C_60144C();                     /* extern */
M2C_UNK func_801D6B14_601EF4(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D6B50_601F30(void *, M2C_UNK);      /* extern */
extern f64 D_8020EE90_63A270;
extern void *D_8020EED0_63A2B0;

void func_802078E0_632CC0(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    f64 temp_f0;

    temp_f0 = (f64) M2C_FIELD(arg0, f32 *, 0x78);
    if (temp_f0 >= 14.0) {
        M2C_FIELD(arg0, f32 *, 0x78) = 14.0f;
    } else {
        M2C_FIELD(arg0, f32 *, 0x78) = (f32) (temp_f0 + D_8020EE90_63A270);
    }
    func_801D606C_60144C();
    func_801D6B14_601EF4(arg0, 0x3DCCCCCD);
    func_801D6B50_601F30(arg0, 0x3DCCCCCD);
    if (M2C_FIELD(arg1, f32 *, 0x10) >= -100.0f) {
        func_80034ED4_35AD4();
        return;
    }
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C4) == 1) {
        func_80034ED4_35AD4();
    }
}
