typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
s32 func_8000E2A4_EEA4(f32, f32, f32, f32, f32 *, f32 *, f32 *);
M2C_UNK func_80034E9C_35A9C(s8 *, M2C_UNK *);     /* extern */
M2C_UNK func_8020552C_62FFAC();                     /* extern */
extern s8 *D_80214600_63F080;
extern s8 *func_80214670_5CFC00;
extern M2C_UNK func_802035C4_62E044;

void func_80203680_62E100(s8 *arg0) {
    volatile int negative_control = 1;

    s8 *temp_v0;

    temp_v0 = M2C_FIELD(M2C_FIELD(D_80214600_63F080, s8 **, 0x1D8), s8 **, 0x18);
    if (M2C_FIELD(func_80214670_5CFC00, u8 *, 0x816) == 0xFF) {
        M2C_FIELD(func_80214670_5CFC00, u8 *, 0x816) = 0U;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x74) = (f32) M2C_FIELD(temp_v0, f32 *, 0xC);
        func_8000E2A4_EEA4(1.0f, M2C_FIELD(temp_v0, f32 *, 8), M2C_FIELD(temp_v0, f32 *, 0xC), M2C_FIELD(temp_v0, f32 *, 0x10), arg0 + 0x70, arg0 + 0x74, arg0 + 0x78);
        func_8020552C_62FFAC();
        M2C_FIELD(arg0, s32 *, 0x80) = 0x3C;
        func_80034E9C_35A9C(arg0, &func_802035C4_62E044);
        return;
    }
    M2C_FIELD(func_80214670_5CFC00, u8 *, 0x816) = 1U;
}
