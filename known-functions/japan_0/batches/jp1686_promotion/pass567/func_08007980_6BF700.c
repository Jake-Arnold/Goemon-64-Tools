#include "../m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_8021DAEC_5D907C;
M2C_UNK func_08007A00_6BF780();                     /* static */

void func_08007980_6BF700(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80038808_39408)(0x8243);
    M2C_FIELD(arg0, s32 *, 0xE8) = (s32) (M2C_FIELD(arg0, s32 *, 0xE8) | 0x80);
    ((M2C_UNK(*)())&func_80023AB0_246B0)(8);
    ((M2C_UNK(*)())&func_8021DAEC_5D907C)(arg0, 0, 0, 0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08007A00_6BF780);
}
