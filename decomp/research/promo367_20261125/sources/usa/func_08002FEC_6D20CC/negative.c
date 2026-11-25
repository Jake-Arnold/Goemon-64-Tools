#include "m2c_types.h"
extern char func_8021927C_5D474C;
extern char func_802197D8_5D4CA8;
extern char func_8021B09C_5D656C;

void func_08002FEC_6D20CC(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_802197D8_5D4CA8)(arg0, 8) == 0) {
        ((M2C_UNK(*)())&func_8021927C_5D474C)(arg0);
        ((M2C_UNK(*)())&func_8021B09C_5D656C)(arg0, 0, 1);
    }
}
