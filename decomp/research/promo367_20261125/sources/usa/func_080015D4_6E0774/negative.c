#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_802197D8_5D4CA8;
extern char func_8021B7AC_5D6C7C;
M2C_UNK func_08001640_6E07E0();                     /* static */

void func_080015D4_6E0774(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_802197D8_5D4CA8)(arg0, 8);
    if (((s32(*)())&func_8021B7AC_5D6C7C)(arg0, 0x42C80000) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02AE87E1;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001640_6E07E0);
    }
}
