#include "m2c_types.h"
extern char func_800143D0_14FD0;
extern M2C_UNK D_A00C980;

s32 func_08001228_6B3168(void) {
    s32 temp_v0;

    temp_v0 = ((s32(*)())&func_800143D0_14FD0)(&D_A00C980, 0x152);
    if (temp_v0 == -1) {
        return 0;
    }
    return temp_v0;
}
