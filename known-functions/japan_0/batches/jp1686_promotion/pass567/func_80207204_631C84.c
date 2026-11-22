#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80037890_38490(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_8003790C_3850C(M2C_UNK, M2C_UNK);      /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_80207268_631CE8();                     /* static */

void func_80207204_631C84(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x7C) = 0x64;
    M2C_FIELD(arg0, s32 *, 0x80) = 1;
    func_80034E8C_35A8C(func_80207268_631CE8);
    func_80038838_39438(0x169);
    func_8003790C_3850C(0, 0x64);
    func_80037890_38490(0, 1, 0x11111111);
}
