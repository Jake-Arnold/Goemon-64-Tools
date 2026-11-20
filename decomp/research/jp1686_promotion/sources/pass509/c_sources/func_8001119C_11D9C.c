#include "m2c_types.h"
void func_8001119C_11D9C(void *arg0, s32 arg1) {
    if (arg0 != NULL) {
        if (arg1 == 0) {
            M2C_FIELD(arg0, s32 *, 0x5C) = 0;
            return;
        }
        M2C_FIELD(arg0, s32 *, 0x5C) = (s32) (arg1 + 0x5C);
    }
}
