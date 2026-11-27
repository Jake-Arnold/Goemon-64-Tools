#include "m2c_types.h"
M2C_UNK func_80218FE8_5D44B8(void *);
extern void *D_801FC628_5B8538;

void func_08002814_6B1C24(void *arg0, M2C_UNK arg1) {
    M2C_UNK (*fn)(void *) = func_80218FE8_5D44B8;
    fn(arg0);
    M2C_FIELD(D_801FC628_5B8538, s8 *, 0x64) = 1;
}
