#include "m2c_types.h"
void func_8021F4D4_5DAA64(s8 *arg0, s32 arg1, s32 arg2, s32 arg3) {
    s8 *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    switch (arg3) {                                 /* irregular */
    case 0:
        M2C_FIELD((temp_v0 + (arg2 * 8)), s32 *, 0x38) = (s32) (M2C_FIELD(temp_v0, s32 *, 0x48) + arg1 + 0xF6000000);
        return;
    case 1:
        M2C_FIELD((temp_v0 + (arg2 * 8)), s32 *, 0x38) = (s32) (M2C_FIELD(temp_v0, s32 *, 0x40) + arg1 + 0xF7000000);
        return;
    case 2:
        M2C_FIELD((temp_v0 + (arg2 * 8)), s32 *, 0x38) = (s32) (M2C_FIELD(temp_v0, s32 *, 0x38) + arg1 + 0xF8000000);
        return;
    }
}
