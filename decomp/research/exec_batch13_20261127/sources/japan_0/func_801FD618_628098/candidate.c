#include "m2c_types.h"
M2C_UNK func_8000F198_FD98(M2C_UNK, void *, void *, M2C_UNK); /* extern */
M2C_UNK func_80034B44_35744();                      /* extern */
M2C_UNK func_801D45B0_5FF030(M2C_UNK);              /* extern */
s32 func_801D8D7C_6037FC(u8 *);                   /* extern */
s32 func_801D8DEC_60386C(u8 *);                   /* extern */
s32 func_801D8F74_6039F4(u8 *);                   /* extern */
M2C_UNK func_801D8FB4_603A34(u8 *);               /* extern */
M2C_UNK func_801D9188_603C08(M2C_UNK);              /* extern */
M2C_UNK func_801DB804_606284(u8 *);               /* extern */
M2C_UNK func_801DBC28_6066A8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801DCB58_6075D8(M2C_UNK, s32, f32, f32); /* extern */
M2C_UNK func_801E726C_611CEC(void *, f32, s32, f32, f32, f32, f32, f32); /* extern */
f32 func_801FC898_627318();                         /* extern */
M2C_UNK func_801FCC14_627694(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern u8 *D_80214600_63F080;

void func_801FD618_628098(void *arg0, void *arg1) {
    f32 sp34;
    u8 *sp30;

    sp30 = D_80214600_63F080 + 0x140;
    sp34 = func_801FC898_627318();
    if (M2C_FIELD(arg0, f32 *, 0x74) > 0.0f) {
        func_801DBC28_6066A8(arg0, 0xBDCCCCCD);
    }
    func_801DB804_606284(arg0);
    if ((sp34 <= M2C_FIELD(arg1, f32 *, 0xC)) && (M2C_FIELD(arg0, s32 *, 0x90) == 0)) {
        M2C_FIELD(arg0, s32 *, 0x90) = 1;
        func_8000F198_FD98(0x286, D_80214600_63F080 + 0xA0, arg1, 0x44BB8000);
        func_801FCC14_627694(arg0, 0x3DCCCCCD, 0x3DA3D70A, 0x3D75C28F);
    }
    if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
        func_80034B44_35744();
    }
    if ((func_801D8D7C_6037FC(arg0) != 0) || (func_801D8DEC_60386C(arg0) != 0)) {
        if (func_801D8F74_6039F4(arg0) >= 0x3C) {
            func_801D9188_603C08(5);
            func_801DCB58_6075D8(5, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10));
        }
        if (func_801D8D7C_6037FC(arg0) == M2C_FIELD(D_80214600_63F080, s32 *, 0x1CC)) {
            if ((M2C_FIELD(sp30, u8 *, 0xE) == 0) && (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C5) == 0)) {
                func_8000F198_FD98(0x106, D_80214600_63F080 + 0xA0, arg1, 0x44BB8000);
            }
        } else {
            func_8000F198_FD98(0x106, D_80214600_63F080 + 0xA0, arg1, 0x44BB8000);
        }
        func_801D45B0_5FF030(4);
        func_801E726C_611CEC(arg0, M2C_FIELD(arg1, f32 *, 0x1C) * 3.0f, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10), 0.0f, 0.0f, 0.0f);
    }
    func_801D8FB4_603A34(arg0);
}
