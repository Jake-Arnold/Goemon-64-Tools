typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D8660_6030E0(void *, f32);
M2C_UNK func_801E52CC_60FD4C(void *, M2C_UNK, M2C_UNK, M2C_UNK, f32, f32, f32, f32, f32, f32);
extern f64 D_80213FF8_63EA78;
extern void *D_80214600_63F080;

void func_801FFF08_62A988(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
        func_801D8660_6030E0(arg1, -100.0f);
        M2C_FIELD(arg0, f32 *, 0x90) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x90) - D_80213FF8_63EA78);
        if (!(M2C_FIELD(D_80214600_63F080, s32 *, 0x2C8) & 0xF)) {
            func_801E52CC_60FD4C(arg0, 8, 0x3F000000, 0x3E4CCCCD, M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg0, f32 *, 0x90), 20.0f, 20.0f, 40.0f);
        }
    } else if (!(M2C_FIELD(D_80214600_63F080, s32 *, 0x2C8) & 7)) {
        func_801E52CC_60FD4C(arg0, 8, 0x3F800000, 0x3F4CCCCD, M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), -470.0f, 20.0f, 20.0f, 20.0f);
    }
}
