#include "m2c_types.h"
void func_801E5E70_654360(void *arg0) {
    if (arg0 != NULL) {
        M2C_FIELD(arg0, s8 *, 0x78) = (s8) (M2C_FIELD(arg0, s8 *, 0x78) & 0xFFFE);
    }
}
