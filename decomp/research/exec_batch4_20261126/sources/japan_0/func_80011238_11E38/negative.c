#include "m2c_types.h"
M2C_UNK func_800111C0_11DC0(void *, u16);

s32 func_80011238_11E38(void *arg0) {
    if (arg0 == NULL) {
        { *(volatile s32 *)0x80000000 = 1; } return 0;
    }
    func_800111C0_11DC0(arg0, M2C_FIELD(arg0, u16 *, 0x20));
    return 0;
}
