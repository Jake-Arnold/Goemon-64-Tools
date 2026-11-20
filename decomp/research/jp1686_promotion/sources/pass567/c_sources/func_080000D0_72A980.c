#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_0800010C_72A9BC();                     /* static */
s32 func_08002BBC_72D46C();                         /* static */

void func_080000D0_72A980(s32 arg0, M2C_UNK arg1) {
    if (func_08002BBC_72D46C() == 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800010C_72A9BC);
    }
}
