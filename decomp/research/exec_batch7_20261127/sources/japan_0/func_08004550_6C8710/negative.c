#include "m2c_types.h"
void func_80034E8C_35A8C(void *); /* extern */
extern M2C_UNK func_08004594_6C8754;

void func_08004550_6C8710(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, u16 *, 0x8A) -= 2;
    if ((s32)M2C_FIELD(arg0, u16 *, 0x8A) <= 0) {
        ((void (*)(void *))func_80034E8C_35A8C)(&func_08004594_6C8754);
    }

    *(volatile s32 *)0x80000000 = 1;
}
