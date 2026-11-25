typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void * func_801E7848_6122C8(void *, f32, s32, f32, f32, f32, f32, f32, u16, u16, u16);
void func_80034B90_35790(void);
void * func_801E726C_611CEC(void *, f32, s32, f32, f32, f32, f32, f32);
void func_801D45B0_5FF030(s32);
s32 func_801D9188_603C08(s32);
u8 func_801D8F74_6039F4(void *);
void func_8000F198_FD98(s32, s32, void *, f32);
M2C_UNK func_801DCB58_6075D8(M2C_UNK, s32, f32, f32); /* extern */
extern s32 D_80214600_63F080;
extern void *func_80214670_5CFC00;

void func_8020B330_635DB0(void *arg0) {
    volatile int negative_control = 1;

    void *temp_s0;

    temp_s0 = M2C_FIELD(arg0, void **, 0x18);
    if (M2C_FIELD(func_80214670_5CFC00, u8 *, 0x11) == 0) {
        M2C_FIELD(func_80214670_5CFC00, u8 *, 0x12) = (u8) (M2C_FIELD(func_80214670_5CFC00, u8 *, 0x12) - 1);
        func_801E726C_611CEC(arg0, M2C_FIELD(temp_s0, f32 *, 0x1C) * 3.0f, M2C_FIELD(temp_s0, s32 *, 8), M2C_FIELD(temp_s0, f32 *, 0xC), M2C_FIELD(temp_s0, f32 *, 0x10), 0.0f, 0.0f, 0.0f);
        func_80034B90_35790();
        return;
    }
    if (M2C_FIELD(arg0, s32 *, 0x38) != 0) {
        M2C_FIELD(func_80214670_5CFC00, u8 *, 0x12) = (u8) (M2C_FIELD(func_80214670_5CFC00, u8 *, 0x12) - 1);
        if (func_801D8F74_6039F4(arg0) >= 0x3C) {
            func_801D9188_603C08(0x14);
            func_801DCB58_6075D8(0x14, M2C_FIELD(temp_s0, s32 *, 8), M2C_FIELD(temp_s0, f32 *, 0xC), M2C_FIELD(temp_s0, f32 *, 0x10));
        }
        func_80034B90_35790();
        func_8000F198_FD98(0x106, D_80214600_63F080 + 0xA0, temp_s0, 1500.0f);
        func_801D45B0_5FF030(0xA);
        func_801E7848_6122C8(arg0, M2C_FIELD(temp_s0, f32 *, 0x1C) * 5.0f, M2C_FIELD(temp_s0, s32 *, 8), M2C_FIELD(temp_s0, f32 *, 0xC), M2C_FIELD(temp_s0, f32 *, 0x10), 0.0f, 0.0f, 0.0f, 0xFFU, 0xFFU, 0xFFU);
    }
}
