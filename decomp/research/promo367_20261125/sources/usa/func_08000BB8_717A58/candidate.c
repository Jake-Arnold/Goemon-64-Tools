#include "m2c_types.h"
extern char func_80012304_12F04;
extern char func_80034EF8_35AF8;
extern char func_8003521C_35E1C;
extern char func_801FC590_5B84A0;
extern void *D_801FC628_5B8538;
extern M2C_UNK func_08000C3C_717ADC;

void func_08000BB8_717A58(void *arg0, void *arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xD0);
    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) | 0x4400);
    arg1 = temp_v0;
    ((M2C_UNK(*)())&func_80012304_12F04)(M2C_FIELD(temp_v0, s32 *, 8));
    ((M2C_UNK(*)())&func_80034EF8_35AF8)(M2C_FIELD(arg1, s32 *, 0xC));
    M2C_FIELD(D_801FC628_5B8538, s8 *, 0x64) = 0;
    ((M2C_UNK(*)())&func_801FC590_5B84A0)();
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000C3C_717ADC);
}
