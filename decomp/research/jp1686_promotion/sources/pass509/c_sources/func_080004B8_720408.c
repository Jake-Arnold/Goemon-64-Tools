#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034B44_35744;
extern char func_80034E8C_35A8C;
M2C_UNK func_080003FC_72034C();                     /* static */

void func_080004B8_720408(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x18) != 0) {
        M2C_FIELD(arg0, s16 *, 0x5E) = 0x2C1;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080003FC_72034C);
        return;
    }
    ((M2C_UNK(*)())&func_80034B44_35744)();
}
