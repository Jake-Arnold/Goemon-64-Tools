#include "m2c_types.h"
s32 func_08000508_728E28(void *);                         /* extern */
extern char func_80034E8C_35A8C;
extern char func_80038838_39438;
extern char func_80226CE0_5E2270;
extern M2C_UNK func_080000E4_728A04;

void func_08000064_728984(void *arg0, M2C_UNK arg1) {
    if (func_08000508_728E28(arg0) != 0) {
        M2C_FIELD(arg0, u8 *, 0xDC) = (u8) (M2C_FIELD(arg0, u8 *, 0xDC) - 1);
        ((M2C_UNK (*)(M2C_UNK))&func_80038838_39438)(0x23C);
        if ((s32) M2C_FIELD(arg0, u8 *, 0xDC) <= 0) {
            ((M2C_UNK (*)())&func_80226CE0_5E2270)();
            M2C_FIELD(arg0, s16 *, 0x8A) = 0;
            ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_080000E4_728A04);
        }
    }
}
