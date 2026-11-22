#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080013B0_6B52B0();                     /* static */
extern s32 D_8005B424;

void func_0800136C_6B526C(void *arg0, M2C_UNK arg1) {
    D_8005B424 = 0;
    M2C_FIELD(arg0, s32 *, 0xD0) = 0xF;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080013B0_6B52B0);
}
