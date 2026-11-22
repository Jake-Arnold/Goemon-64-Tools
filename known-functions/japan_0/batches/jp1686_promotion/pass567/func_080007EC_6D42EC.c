#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08000828_6D4328();                     /* static */

void func_080007EC_6D42EC(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x27;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000828_6D4328);
}
