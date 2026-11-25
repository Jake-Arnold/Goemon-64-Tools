#include "m2c_types.h"
extern char func_80011E94_12A94;
extern char func_80034B68_35768;
extern char func_80034E8C_35A8C;
extern void *D_80201534_5BD504;
extern void *D_80201538_5BD508;
extern M2C_UNK func_0800195C_71CD1C;

void func_080018D4_71CC94(void *arg0, void *arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xD0);
    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) | 0x4400);
    M2C_FIELD(D_80201534_5BD504, s8 *, 0xD0) = 0x1E;
    arg1 = temp_v0;
    ((M2C_UNK(*)())&func_80011E94_12A94)(M2C_FIELD(temp_v0, s32 *, 8));
    ((M2C_UNK(*)())&func_80034B68_35768)(M2C_FIELD(arg1, s32 *, 0xC));
    M2C_FIELD(D_80201538_5BD508, s8 *, 0x64) = 0;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_0800195C_71CD1C);
}
