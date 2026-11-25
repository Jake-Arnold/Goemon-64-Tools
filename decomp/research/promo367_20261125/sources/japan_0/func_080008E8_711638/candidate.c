#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern M2C_UNK func_0800093C_71168C;

void func_080008E8_711638(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~1);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_0800093C_71168C);
    }
}
