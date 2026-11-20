#include "../m2c_types.h"
s32 func_80229D70_5E5300(void *);                   /* extern */
s32 func_8022ABD0_5E6160();                         /* static */
M2C_UNK func_8022B2F0_5E6880(void *, u16, s32);     /* static */

s32 func_8022B494_5E6A24(void *arg0) {
    s32 sp18;
    s32 temp_v0;

    temp_v0 = func_8022ABD0_5E6160();
    sp18 = temp_v0;
    func_8022B2F0_5E6880(arg0, M2C_FIELD(arg0, u16 *, 0xEA), func_80229D70_5E5300(arg0) & 0xFFFF);
    return temp_v0;
}
