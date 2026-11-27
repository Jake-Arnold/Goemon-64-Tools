#include "m2c_types.h"
M2C_UNK func_8021DD58_5D92E8(void *);
extern void *D_80201538_5BD508;

void func_08002800_6B6700(void *arg0, M2C_UNK arg1) {
    M2C_UNK (*fn)(void *) = func_8021DD58_5D92E8;
    fn(arg0);
    M2C_FIELD(D_80201538_5BD508, s8 *, 0x64) = 1;
}
