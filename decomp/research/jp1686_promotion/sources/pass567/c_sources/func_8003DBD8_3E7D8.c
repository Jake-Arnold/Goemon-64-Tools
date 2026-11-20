#include "../m2c_types.h"
extern s32 D_801CCED0_1CDAD0;

s32 func_8003DBD8_3E7D8(void) {
    if (D_801CCED0_1CDAD0 >= 2) {
        D_801CCED0_1CDAD0 -= 1;
        return 1;
    }
    return 0;
}
