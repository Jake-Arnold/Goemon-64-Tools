#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80220168_5DB638;
extern char func_8022026C_5DB73C;
M2C_UNK func_08004BBC_6F809C();                     /* static */

void func_08004B58_6F8038(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_80220168_5DB638)(arg0, 0x50) == 0) {
        ((M2C_UNK(*)())&func_8022026C_5DB73C)(arg0, 0xFF, 0xFF, 0xFF);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08004BBC_6F809C);
    }
}
