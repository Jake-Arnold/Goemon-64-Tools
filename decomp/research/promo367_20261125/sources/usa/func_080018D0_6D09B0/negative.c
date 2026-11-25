#include "m2c_types.h"
extern char func_8003521C_35E1C;
s32 func_080016A8_6D0788();                         /* static */
M2C_UNK func_0800191C_6D09FC();                     /* static */

void func_080018D0_6D09B0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if ((func_080016A8_6D0788() == 0) && !(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800191C_6D09FC);
    }
}
