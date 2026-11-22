#include "m2c_types.h"
extern char func_80034B44_35744;
extern char func_80038808_39408;

void func_08003008_6B6F08(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80038808_39408)(M2C_FIELD(arg0, u16 *, 0xD2));
    ((M2C_UNK(*)())&func_80034B44_35744)();
}
