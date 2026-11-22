#include "../m2c_types.h"
void func_08000298_6C4458(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x8000) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) = 0x82800320;
}
