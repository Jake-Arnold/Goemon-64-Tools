typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034ED4_35AD4();                      /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
f32 func_801D2F40_5FE320(void *, M2C_UNK, void *);  /* extern */
M2C_UNK func_801D614C_60152C(void *);               /* extern */
extern f64 D_8020EEB8_63A298;
extern f64 D_8020EEC0_63A2A0;

void func_80209870_634C50(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    if (func_801D2F40_5FE320(arg1, 0x42700000, arg0) == 0.0f) {
        if (M2C_FIELD(arg0, s32 *, 0x90) == 0) {
            func_80038BC8_397C8(0x14E);
            M2C_FIELD(arg0, s32 *, 0x90) = 1;
        }
        M2C_FIELD(arg0, f32 *, 0x74) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x74) + D_8020EEB8_63A298);
        if ((f64) M2C_FIELD(arg0, f32 *, 0x74) >= 2.0) {
            M2C_FIELD(arg0, f32 *, 0x74) = 2.0f;
        }
        M2C_FIELD(arg0, f32 *, 0x78) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x78) + D_8020EEC0_63A2A0);
        if ((f64) M2C_FIELD(arg0, f32 *, 0x78) >= 10.0) {
            M2C_FIELD(arg0, f32 *, 0x78) = 10.0f;
        }
        func_801D614C_60152C(arg0);
        if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
            func_80034ED4_35AD4();
        }
    }
}
