#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80220168_5DB638;
M2C_UNK func_080036CC_7047CC();                     /* static */

void func_08003678_704778(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_80220168_5DB638)(arg0, 0x50) == 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 5;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080036CC_7047CC);
    }
}
