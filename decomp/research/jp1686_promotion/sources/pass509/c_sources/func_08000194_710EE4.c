#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_08000204_710F54();                     /* static */
M2C_UNK func_08000298_710FE8();                     /* static */

void func_08000194_710EE4(void *arg0, M2C_UNK arg1) {
    if ((M2C_FIELD(arg0, u8 *, 0xD4) == 1) && (((s32(*)())&func_80023D9C_2499C)(M2C_FIELD(arg0, u16 *, 0xD0)) != 0)) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000298_710FE8);
        return;
    }
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000204_710F54);
}
