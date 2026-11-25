typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
s8 * func_801E726C_611CEC(s8 *, f32, s32, f32, f32, f32, f32, f32);
void func_801D45B0_5FF030(s32);
s32 func_801D9188_603C08(s32);
u8 func_801D8F74_6039F4(s8 *);
void func_8000F198_FD98(s32, s32, s8 *, f32);
s32 func_801D8D7C_6037FC(s8 *);                   /* extern */
M2C_UNK func_801DCB58_6075D8(M2C_UNK, s32, f32, f32); /* extern */
extern s8 *D_80214600_63F080;

void func_801EFD44_61A7C4(s8 *arg0) {
    volatile int negative_control = 1;

    s8 *temp_s0;

    s8 *sp30;
    sp30 = D_80214600_63F080 + 0x140;
    if (arg0 != NULL) {
        temp_s0 = M2C_FIELD(arg0, s8 **, 0x18);
        if (temp_s0 != NULL) {
            if (func_801D8F74_6039F4(arg0) >= 0x3C) {
                func_801D9188_603C08(5);
                func_801DCB58_6075D8(5, M2C_FIELD(temp_s0, s32 *, 8), M2C_FIELD(temp_s0, f32 *, 0xC), M2C_FIELD(temp_s0, f32 *, 0x10));
            }
            if (func_801D8D7C_6037FC(arg0) == M2C_FIELD(D_80214600_63F080, s32 *, 0x1CC)) {
                if ((M2C_FIELD(sp30, u8 *, 0xE) == 0) && (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C5) == 0)) {
                    func_8000F198_FD98(0x106, (s32) (D_80214600_63F080 + 0xA0), temp_s0, 1500.0f);
                }
            } else {
                func_8000F198_FD98(0x106, (s32) (D_80214600_63F080 + 0xA0), temp_s0, 1500.0f);
            }
            func_801D45B0_5FF030(4);
            func_801E726C_611CEC(arg0, M2C_FIELD(temp_s0, f32 *, 0x1C) * 3.0f, M2C_FIELD(temp_s0, s32 *, 8), M2C_FIELD(temp_s0, f32 *, 0xC), M2C_FIELD(temp_s0, f32 *, 0x10), 0.0f, 0.0f, 0.0f);
        }
    }
}
