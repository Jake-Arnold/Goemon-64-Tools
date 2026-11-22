#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08000CCC_70049C();                     /* static */

void func_08000E28_7005F8(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0xD4) = (s16) M2C_FIELD(arg0, u8 *, 0xD1);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000CCC_70049C);
}
