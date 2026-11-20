#include "../m2c_types.h"
M2C_UNK func_80034B68_35768(void *);                /* extern */
M2C_UNK func_80038808_39408(s32);                   /* extern */

s32 func_8000F968_10568(void *arg0) {
    func_80038808_39408((M2C_FIELD(arg0, u16 *, 0x5C) | 0x8000) & 0xFFFF);
    func_80034B68_35768(arg0);
    return 0;
}
