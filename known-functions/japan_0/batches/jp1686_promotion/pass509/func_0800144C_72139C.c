#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_08000284_7201D4();                     /* static */
M2C_UNK func_08001390_7212E0();                     /* static */

void func_0800144C_72139C(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x18, arg0) != 0) {
        M2C_FIELD(arg0, s16 *, 0x5E) = 0x2BF;
        M2C_FIELD(arg0, s32 *, 0xD4) = 0x14E;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000284_7201D4, arg0);
        return;
    }
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x2C5;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001390_7212E0, arg0);
}
