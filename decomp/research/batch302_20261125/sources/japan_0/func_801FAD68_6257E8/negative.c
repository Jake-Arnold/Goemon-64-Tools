typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D8660_6030E0(void *, f32);
void func_801F5C70_6206F0(void *);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801FC76C_6271EC();                     /* extern */
extern M2C_UNK func_801FC0B8_626B38;

void func_801FAD68_6257E8(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + 2.0f);
    if (func_801D8660_6030E0(arg1, -120.0f) == 0.0f) {
        if (M2C_FIELD(arg0, s32 *, 0xE8) >= 2) {
            M2C_FIELD(arg0, s32 *, 0xE8) = 0;
            M2C_FIELD(arg0, s32 *, 0xE0) = 0;
            func_801FC76C_6271EC();
            func_80034E8C_35A8C(&func_801FC0B8_626B38);
            return;
        }
        func_801F5C70_6206F0(arg0);
    }
}
