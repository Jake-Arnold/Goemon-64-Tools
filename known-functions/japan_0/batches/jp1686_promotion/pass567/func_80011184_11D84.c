#include "../m2c_types.h"
void func_80011184_11D84(s32 arg0, s32 arg1, s32 arg2) {
    void *temp_v0;

    temp_v0 = arg0 + 0x5C;
    if (arg0 != 0) {
        M2C_FIELD(temp_v0, s32 *, 8) = arg1;
        M2C_FIELD(temp_v0, s32 *, 0xC) = arg2;
    }
}
