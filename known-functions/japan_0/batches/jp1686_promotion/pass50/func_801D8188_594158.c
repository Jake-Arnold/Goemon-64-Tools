#include "m2c_types.h"
f32 func_80003C58_4858(u16);                        /* extern */
M2C_UNK func_801D8284_594254(void *, s32);          /* static */
M2C_UNK func_801D830C_5942DC(void *, f32);          /* static */

void func_801D8188_594158(void *arg0, s32 arg1) {
    func_801D830C_5942DC(arg0, M2C_FIELD(arg0, f32 *, 0x74) * func_80003C58_4858(M2C_FIELD(arg0, u16 *, 0x6E)));
    func_801D8284_594254(arg0, arg1);
}
