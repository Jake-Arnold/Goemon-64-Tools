#include "m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
extern M2C_UNK func_080008E8_70D108;
extern M2C_UNK func_08000A8C_70D2AC;

void func_08000854_70D074(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
    if (((s32(*)())&func_80023E94_24A94)(M2C_FIELD(arg0, u16 *, 0xD0), arg0) != 0) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080008E8_70D108, arg0);
        return;
    }
    M2C_FIELD(arg0, M2C_UNK **, 0xBC) = &func_080008E8_70D108;
    ((M2C_UNK(*)())&func_80023DF0_249F0)(M2C_FIELD(arg0, u16 *, 0xD0), arg0);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000A8C_70D2AC);
}
