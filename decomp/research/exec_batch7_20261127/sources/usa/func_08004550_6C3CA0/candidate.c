#include "m2c_types.h"
void func_8003521C_35E1C(void *); /* extern */
extern M2C_UNK func_08004594_6C3CE4;

void func_08004550_6C3CA0(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, u16 *, 0x8A) -= 2;
    if ((s32)M2C_FIELD(arg0, u16 *, 0x8A) <= 0) {
        ((void (*)(void *))func_8003521C_35E1C)(&func_08004594_6C3CE4);
    }
}
