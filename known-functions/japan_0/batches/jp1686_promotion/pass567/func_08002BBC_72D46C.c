#include "../m2c_types.h"
extern char func_80013820_14420;
extern M2C_UNK D_08002C7C_72D52C;

s32 func_08002BBC_72D46C(void) {
    if (((s32(*)())&func_80013820_14420)(&D_08002C7C_72D52C, 1) == 0) {
        return 1;
    }
    return 0;
}
