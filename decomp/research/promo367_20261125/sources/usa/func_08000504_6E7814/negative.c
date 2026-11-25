#include "../m2c_types.h"
extern char func_8021927C_5D474C;
extern char func_8021B09C_5D656C;

void func_08000504_6E7814(s32 arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg1, u16 *, 0x16) = (u16) (M2C_FIELD(arg1, u16 *, 0x16) + 2);
    ((M2C_UNK(*)())&func_8021927C_5D474C)(arg0);
    ((M2C_UNK(*)())&func_8021B09C_5D656C)(arg0, 1, 0);
}
