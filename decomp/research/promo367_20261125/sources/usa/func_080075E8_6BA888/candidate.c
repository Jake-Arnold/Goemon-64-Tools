#include "m2c_types.h"
extern char func_0800A04C_6BD2EC;
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_802197D8_5D4CA8;
extern M2C_UNK func_08007694_6BA934;
extern M2C_UNK func_080079B0_6BAC50;

void func_080075E8_6BA888(void *arg0, M2C_UNK arg1) {
    s32 temp_v1;

    if (((s32(*)())&func_80023E94_24A94)(0xB) != 0) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080079B0_6BAC50);
        return;
    }
    ((M2C_UNK(*)())&func_0800A04C_6BD2EC)(arg0);
    ((M2C_UNK(*)())&func_802197D8_5D4CA8)(arg0, 1);
    temp_v1 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v1 - 1);
    if (temp_v1 == 0) {
        ((M2C_UNK(*)())&func_80038B98_39798)(0x8203);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08007694_6BA934);
    }
}
