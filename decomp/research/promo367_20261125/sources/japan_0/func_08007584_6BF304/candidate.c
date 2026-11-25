#include "m2c_types.h"
extern char func_08009FE8_6C1D68;
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_8021E548_5D9AD8;
extern M2C_UNK func_08007630_6BF3B0;
extern M2C_UNK func_0800794C_6BF6CC;

void func_08007584_6BF304(void *arg0, M2C_UNK arg1) {
    s32 temp_v1;

    if (((s32(*)())&func_80023B54_24754)(0xB) != 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_0800794C_6BF6CC);
        return;
    }
    ((M2C_UNK(*)())&func_08009FE8_6C1D68)(arg0);
    ((M2C_UNK(*)())&func_8021E548_5D9AD8)(arg0, 1);
    temp_v1 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v1 - 1);
    if (temp_v1 == 0) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x8203);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08007630_6BF3B0);
    }
}
