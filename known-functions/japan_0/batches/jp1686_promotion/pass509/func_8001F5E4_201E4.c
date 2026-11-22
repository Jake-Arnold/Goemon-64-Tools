#include "m2c_types.h"
M2C_UNK func_8000339C_3F9C();                       /* extern */
M2C_UNK func_80020110_20D10();                      /* extern */
extern M2C_UNK g_system;

void func_8001F5E4_201E4(void) {
    func_80020110_20D10();
    M2C_FIELD(&g_system, s16 *, 0x3ADB6) = 0;
    func_8000339C_3F9C();
}
