#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021E548_5D9AD8;
M2C_UNK func_08000240_6D8640();                     /* static */

void func_080001EC_6D85EC(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_8021E548_5D9AD8)(arg0, 8) == 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x28;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000240_6D8640);
    }
}
