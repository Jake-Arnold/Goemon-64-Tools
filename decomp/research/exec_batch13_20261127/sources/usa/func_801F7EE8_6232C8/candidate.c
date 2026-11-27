#include "m2c_types.h"
M2C_UNK func_8000F3D8_FFD8(M2C_UNK, void *, void *, M2C_UNK); /* extern */
M2C_UNK func_80034ED4_35AD4();                      /* extern */
M2C_UNK func_801CEE80_5FA260(M2C_UNK);              /* extern */
s32 func_801D365C_5FEA3C(u8 *);                   /* extern */
s32 func_801D36CC_5FEAAC(u8 *);                   /* extern */
s32 func_801D3854_5FEC34(u8 *);                   /* extern */
M2C_UNK func_801D3894_5FEC74(u8 *);               /* extern */
M2C_UNK func_801D3A68_5FEE48(M2C_UNK);              /* extern */
M2C_UNK func_801D60E4_6014C4(u8 *);               /* extern */
M2C_UNK func_801D6508_6018E8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D7438_602818(M2C_UNK, s32, f32, f32); /* extern */
M2C_UNK func_801E1B30_60CF10(void *, f32, s32, f32, f32, f32, f32, f32); /* extern */
f32 func_801F7168_622548();                         /* extern */
M2C_UNK func_801F74E4_6228C4(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern u8 *D_8020EED0_63A2B0;

void func_801F7EE8_6232C8(void *arg0, void *arg1) {
    f32 sp34;
    u8 *sp30;

    sp30 = D_8020EED0_63A2B0 + 0x140;
    sp34 = func_801F7168_622548();
    if (M2C_FIELD(arg0, f32 *, 0x74) > 0.0f) {
        func_801D6508_6018E8(arg0, 0xBDCCCCCD);
    }
    func_801D60E4_6014C4(arg0);
    if ((sp34 <= M2C_FIELD(arg1, f32 *, 0xC)) && (M2C_FIELD(arg0, s32 *, 0x90) == 0)) {
        M2C_FIELD(arg0, s32 *, 0x90) = 1;
        func_8000F3D8_FFD8(0x286, D_8020EED0_63A2B0 + 0xA0, arg1, 0x44BB8000);
        func_801F74E4_6228C4(arg0, 0x3DCCCCCD, 0x3DA3D70A, 0x3D75C28F);
    }
    if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
        func_80034ED4_35AD4();
    }
    if ((func_801D365C_5FEA3C(arg0) != 0) || (func_801D36CC_5FEAAC(arg0) != 0)) {
        if (func_801D3854_5FEC34(arg0) >= 0x3C) {
            func_801D3A68_5FEE48(5);
            func_801D7438_602818(5, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10));
        }
        if (func_801D365C_5FEA3C(arg0) == M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1CC)) {
            if ((M2C_FIELD(sp30, u8 *, 0xE) == 0) && (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C5) == 0)) {
                func_8000F3D8_FFD8(0x106, D_8020EED0_63A2B0 + 0xA0, arg1, 0x44BB8000);
            }
        } else {
            func_8000F3D8_FFD8(0x106, D_8020EED0_63A2B0 + 0xA0, arg1, 0x44BB8000);
        }
        func_801CEE80_5FA260(4);
        func_801E1B30_60CF10(arg0, M2C_FIELD(arg1, f32 *, 0x1C) * 3.0f, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10), 0.0f, 0.0f, 0.0f);
    }
    func_801D3894_5FEC74(arg0);
}
