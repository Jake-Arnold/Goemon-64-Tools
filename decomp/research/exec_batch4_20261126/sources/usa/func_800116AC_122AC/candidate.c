#include "m2c_types.h"
M2C_UNK func_80011634_12234(void *, u16);

s32 func_800116AC_122AC(void *arg0) {
    if (arg0 == NULL) {
        return 0;
    }
    func_80011634_12234(arg0, M2C_FIELD(arg0, u16 *, 0x20));
    return 0;
}
