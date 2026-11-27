#include "m2c_types.h"
s32 func_08000508_724A08(void *);                         /* extern */
extern char func_8003521C_35E1C;
extern char func_80038BC8_397C8;
extern char func_80221F70_5DD440;
extern M2C_UNK func_080000E4_7245E4;

void func_08000064_724564(void *arg0, M2C_UNK arg1) {
    if (func_08000508_724A08(arg0) != 0) {
        M2C_FIELD(arg0, u8 *, 0xDC) = (u8) (M2C_FIELD(arg0, u8 *, 0xDC) - 1);
        ((M2C_UNK (*)(M2C_UNK))&func_80038BC8_397C8)(0x23C);
        if ((s32) M2C_FIELD(arg0, u8 *, 0xDC) <= 0) {
            ((M2C_UNK (*)())&func_80221F70_5DD440)();
            M2C_FIELD(arg0, s16 *, 0x8A) = 0;
            ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080000E4_7245E4);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
