#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_801FA3FC_5B630C;
extern char func_80216DF8_5D22C8;
extern M2C_UNK func_0800221C_6C196C;
extern M2C_UNK func_08002488_6C1BD8;

void func_0800211C_6C186C(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_800240DC_24CDC)(0x15A) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x802006E1;
        ((M2C_UNK(*)())&func_80216DF8_5D22C8)(arg0, 1);
        ((M2C_UNK(*)())&func_801FA3FC_5B630C)(0xFF, 0xFF, 0xFF);
        M2C_FIELD(arg0, s8 *, 0x6C) = 1;
        M2C_FIELD(arg0, s8 *, 0x4C) = 0;
        ((M2C_UNK(*)())&func_80038B98_39798)(0x2AD);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08002488_6C1BD8);
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) = 0x802006E1;
    ((M2C_UNK(*)())&func_80216DF8_5D22C8)(arg0, 0);
    ((M2C_UNK(*)())&func_801FA3FC_5B630C)(0x78, 0x78, 0xFF);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s8 *, 0x4C) = 0;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_0800221C_6C196C);
}
