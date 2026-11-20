#include "../m2c_types.h"
M2C_UNK func_8021EBE0_5DA170(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_8022A928_5E5EB8();                     /* extern */

void func_8022B4D4_5E6A64(void *arg0) {
    void *sp1C;

    M2C_FIELD(arg0, s32 *, 0x60) = 0x261;
    M2C_FIELD(arg0, s32 *, 0x64) = 0x20;
    sp1C = M2C_FIELD(arg0, void **, 0x18);
    func_8022A928_5E5EB8();
    M2C_FIELD(arg0, s16 *, 0xE4) = (s16) (s32) M2C_FIELD(sp1C, f32 *, 0xC);
    func_8021EBE0_5DA170(arg0, 5, 0);
}
