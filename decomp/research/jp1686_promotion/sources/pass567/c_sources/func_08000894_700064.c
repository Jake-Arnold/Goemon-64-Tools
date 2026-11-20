#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080007C0_6FFF90();                     /* static */

void func_08000894_700064(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0xD8) = (s16) (M2C_FIELD(arg0, u8 *, 0xD1) * 4);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080007C0_6FFF90);
}
