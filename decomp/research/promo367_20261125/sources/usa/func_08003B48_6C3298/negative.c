#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern M2C_UNK func_08003C7C_6C33CC;

void func_08003B48_6C3298(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    u8 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u8 *, 0xD0);
    if (temp_v0 == 0) {
        if (((s32(*)())&func_800240DC_24CDC)(M2C_FIELD(arg0, u16 *, 0xD4), arg0) != 0) {
            ((M2C_UNK(*)())&func_80038B98_39798)(0x154);
            ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08003C7C_6C33CC);
        }
    } else if (temp_v0 == 1) {
        if (((s32(*)())&func_800240DC_24CDC)(M2C_FIELD(arg0, u16 *, 0xD4), arg0) != 0) {
            ((M2C_UNK(*)())&func_80038B98_39798)(0x154);
            ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08003C7C_6C33CC);
        }
    } else if (((temp_v0 == 2) || (temp_v0 == 3) || (temp_v0 == 4) || (temp_v0 == 5) || (temp_v0 == 6) || (temp_v0 == 7)) && (((s32(*)())&func_800240DC_24CDC)(M2C_FIELD(arg0, u16 *, 0xD4), arg0) != 0)) {
        if (M2C_FIELD(arg0, u8 *, 0xD0) == 2) {
            ((M2C_UNK(*)())&func_80038B98_39798)(0x154, arg0);
        }
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08003C7C_6C33CC);
    }
}
