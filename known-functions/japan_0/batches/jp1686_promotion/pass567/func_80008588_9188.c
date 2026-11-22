#include "../m2c_types.h"
extern M2C_UNK g_system;

void func_80008588_9188(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, s32 *, 0x34) = arg1;
    M2C_FIELD(arg0, s32 *, 0x14) = (s32) M2C_FIELD(&g_system, s32 *, 0xC5F78);
}
