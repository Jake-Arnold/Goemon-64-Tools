#include "m2c_types.h"
M2C_UNK func_801E962C_5A55FC();                     /* extern */
M2C_UNK func_801FABE0_5B6BB0(M2C_UNK, M2C_UNK);              /* extern */

void func_801E390C_59F8DC(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u8 *, 0x60) == 2) {
        func_801FABE0_5B6BB0(arg0, 7);
        return;
    }
    func_801E962C_5A55FC();
}
