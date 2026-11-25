#include "m2c_types.h"
extern char func_80023CF8_248F8;
extern char func_80034E8C_35A8C;
extern char func_8003CF80_3DB80;
extern char func_8021CDBC_5D834C;
extern char func_8021DB18_5D90A8;
extern char func_8021EF9C_5DA52C;
extern char func_80226CE0_5E2270;
extern M2C_UNK func_080078A0_6CBA60;

void func_080077C8_6CB988(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 4) & 0x3FF);
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x200) {
        ((M2C_UNK(*)())&func_80226CE0_5E2270)();
        ((M2C_UNK(*)())&func_8003CF80_3DB80)(0x85);
        ((M2C_UNK(*)())&func_80023CF8_248F8)(0x1A5);
        ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0, 0, 0);
        ((M2C_UNK(*)())&func_8021EF9C_5DA52C)(arg0);
        M2C_FIELD(arg0, s32 *, 0x60) = 0;
        ((M2C_UNK(*)())&func_8021CDBC_5D834C)(arg0, 0);
        temp_v0 = M2C_FIELD(arg0, void **, 0xE4);
        if (temp_v0 != NULL) {
            M2C_FIELD(temp_v0, s8 *, 0xD0) = 1;
        }
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_080078A0_6CBA60);
    }
}
