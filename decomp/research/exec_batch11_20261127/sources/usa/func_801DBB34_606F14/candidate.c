#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801D620C_6015EC(M2C_UNK, s32, s32, s32);
M2C_UNK func_801DBFB4_607394(void *, s32, s32, M2C_UNK);
extern M2C_UNK func_801DBBE8_606FC8;

void func_801DBB34_606F14(void *arg0, M2C_UNK arg1) {
    func_801D620C_6015EC(arg1, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x74), M2C_FIELD(arg0, s32 *, 0x78));
    M2C_FIELD(arg0, f32 *, 0x9C) += M2C_FIELD(arg0, f32 *, 0xA8);
    M2C_FIELD(arg0, f32 *, 0xA0) += M2C_FIELD(arg0, f32 *, 0xAC);
    M2C_FIELD(arg0, f32 *, 0xA4) += M2C_FIELD(arg0, f32 *, 0xB0);
    func_801DBFB4_607394(arg0, M2C_FIELD(arg0, s32 *, 0x84), ++M2C_FIELD(arg0, s32 *, 0x88), 0x41200000);
    if (M2C_FIELD(arg0, s32 *, 0x7C)-- < 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x3C;
        M2C_FIELD(arg0, s32 *, 0x80) = 0xFF;
        func_8003521C_35E1C(&func_801DBBE8_606FC8);
    }
}
