#include "m2c_types.h"
extern char func_8000F52C_1012C;
extern char func_8003521C_35E1C;
M2C_UNK func_08001368_6FC568();                     /* static */
extern M2C_UNK D_8020CBF0_5C8B00;

void func_080012DC_6FC4DC(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (M2C_FIELD(arg0, u16 *, 0xD4) != 0) {
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) (M2C_FIELD(arg1, u16 *, 0x14) + 8);
    } else {
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) (M2C_FIELD(arg1, u16 *, 0x14) - 8);
    }
    if (!(M2C_FIELD(arg1, u16 *, 0x14) & 0x1FF)) {
        ((M2C_UNK(*)())&func_8000F52C_1012C)(0x2A0, &D_8020CBF0_5C8B00, arg1, 0x44480000);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x64;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001368_6FC568);
    }
}
