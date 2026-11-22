#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_0800234C_6F9EDC();                     /* static */

void func_08002304_6F9E94(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(M2C_FIELD(arg0, u16 *, 0xD0)) != 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800234C_6F9EDC);
    }
}
