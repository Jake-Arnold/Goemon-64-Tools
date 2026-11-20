#include "../m2c_types.h"
void func_08001CC4_6EF524(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, s32 *, 0xD0) != 0) {
        M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 2) & 0x3FF);
        return;
    }
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) - 2) & 0x3FF);
}
