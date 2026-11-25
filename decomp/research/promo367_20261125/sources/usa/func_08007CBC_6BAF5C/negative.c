#include "m2c_types.h"
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
extern M2C_UNK func_080073FC_6BA69C;
extern M2C_UNK func_080079B0_6BAC50;

void func_08007CBC_6BAF5C(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        if (((s32(*)())&func_80023E94_24A94)(0xB) != 0) {
            ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080079B0_6BAC50);
        }
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080073FC_6BA69C);
    }
}
