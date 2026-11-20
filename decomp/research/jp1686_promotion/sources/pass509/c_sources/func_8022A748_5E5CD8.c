#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_8021EBE0_5DA170(void *, M2C_UNK, M2C_UNK); /* extern */
s32 func_8022A118_5E56A8();                         /* static */
M2C_UNK func_8022A6C4_5E5C54();                     /* static */

void func_8022A748_5E5CD8(void *arg0, M2C_UNK arg1) {
    void *sp1C;

    sp1C = M2C_FIELD(arg0, void **, 0x18);
    if (func_8022A118_5E56A8() != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x12800761;
        M2C_FIELD(arg0, s32 *, 0x64) = 0x20;
        M2C_FIELD(arg0, s16 *, 0xE4) = (s16) (s32) M2C_FIELD(sp1C, f32 *, 0xC);
        func_8021EBE0_5DA170(arg0, 5, 0);
        func_80034E8C_35A8C(func_8022A6C4_5E5C54);
    }
}
