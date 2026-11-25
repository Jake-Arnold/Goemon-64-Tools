#include "m2c_types.h"
extern char func_80024038_24C38;
extern char func_8003521C_35E1C;
extern char func_8003D310_3DF10;
extern char func_8021804C_5D351C;
extern char func_80218DA8_5D4278;
extern char func_8021A22C_5D56FC;
extern char func_80221F70_5DD440;
extern M2C_UNK func_080078A0_6C6FF0;

void func_080077C8_6C6F18(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 4) & 0x3FF);
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x200) {
        ((M2C_UNK(*)())&func_80221F70_5DD440)();
        ((M2C_UNK(*)())&func_8003D310_3DF10)(0x85);
        ((M2C_UNK(*)())&func_80024038_24C38)(0x1A5);
        ((M2C_UNK(*)())&func_80218DA8_5D4278)(arg0, 0, 0, 0);
        ((M2C_UNK(*)())&func_8021A22C_5D56FC)(arg0);
        M2C_FIELD(arg0, s32 *, 0x60) = 0;
        ((M2C_UNK(*)())&func_8021804C_5D351C)(arg0, 0);
        temp_v0 = M2C_FIELD(arg0, void **, 0xE4);
        if (temp_v0 != NULL) {
            M2C_FIELD(temp_v0, s8 *, 0xD0) = 1;
        }
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080078A0_6C6FF0);
    }
}
