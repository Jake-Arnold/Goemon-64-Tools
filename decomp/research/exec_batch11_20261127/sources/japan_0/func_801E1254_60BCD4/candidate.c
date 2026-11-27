#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_801DB92C_6063AC(M2C_UNK, s32, s32, s32);
M2C_UNK func_801E16D4_60C154(void *, s32, s32, M2C_UNK);
extern M2C_UNK func_801E1308_60BD88;

void func_801E1254_60BCD4(void *arg0, M2C_UNK arg1) {
    func_801DB92C_6063AC(arg1, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x74), M2C_FIELD(arg0, s32 *, 0x78));
    M2C_FIELD(arg0, f32 *, 0x9C) += M2C_FIELD(arg0, f32 *, 0xA8);
    M2C_FIELD(arg0, f32 *, 0xA0) += M2C_FIELD(arg0, f32 *, 0xAC);
    M2C_FIELD(arg0, f32 *, 0xA4) += M2C_FIELD(arg0, f32 *, 0xB0);
    func_801E16D4_60C154(arg0, M2C_FIELD(arg0, s32 *, 0x84), ++M2C_FIELD(arg0, s32 *, 0x88), 0x41200000);
    if (M2C_FIELD(arg0, s32 *, 0x7C)-- < 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x3C;
        M2C_FIELD(arg0, s32 *, 0x80) = 0xFF;
        func_80034E8C_35A8C(&func_801E1308_60BD88);
    }
}
