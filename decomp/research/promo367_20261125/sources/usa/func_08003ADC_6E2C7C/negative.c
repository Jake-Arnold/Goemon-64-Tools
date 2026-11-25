#include "m2c_types.h"
extern char func_8021927C_5D474C;
extern char func_8021B09C_5D656C;

void func_08003ADC_6E2C7C(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8021927C_5D474C)();
        ((M2C_UNK(*)())&func_8021B09C_5D656C)(arg0, 0, 1);
    }
}
