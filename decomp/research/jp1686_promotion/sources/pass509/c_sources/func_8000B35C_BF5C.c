#include "m2c_types.h"
M2C_UNK func_8000B39C_BF9C();                       /* extern */
M2C_UNK func_8000B3E4_BFE4();                       /* extern */
extern M2C_UNK g_system;

void func_8000B35C_BF5C(void) {
    if (M2C_FIELD(&g_system, u8 *, 0xCF88D) == 0x80) {
        func_8000B39C_BF9C();
        return;
    }
    func_8000B3E4_BFE4();
}
