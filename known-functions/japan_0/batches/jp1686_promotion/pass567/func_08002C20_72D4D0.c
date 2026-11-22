#include "../m2c_types.h"
extern char func_80013820_14420;
extern M2C_UNK D_08002C80_72D530;

s32 func_08002C20_72D4D0(void) {
    if (((s32(*)())&func_80013820_14420)(&D_08002C80_72D530, 1) == 0) {
        return 1;
    }
    return 0;
}
