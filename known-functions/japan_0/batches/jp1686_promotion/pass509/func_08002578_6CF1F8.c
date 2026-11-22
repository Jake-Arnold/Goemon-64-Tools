#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_08000920_6CD5A0();                     /* static */

void func_08002578_6CF1F8(s32 arg0, void *arg1) {
    if ((((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) && (M2C_FIELD(arg1, u8 *, 0x7C) & 2)) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000920_6CD5A0);
    }
}
