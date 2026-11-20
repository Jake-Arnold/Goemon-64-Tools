#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_08007C58_6BF9D8();                     /* static */

void func_08007C0C_6BF98C(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
    ((M2C_UNK(*)())&func_80038808_39408)(0x8251);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08007C58_6BF9D8);
}
