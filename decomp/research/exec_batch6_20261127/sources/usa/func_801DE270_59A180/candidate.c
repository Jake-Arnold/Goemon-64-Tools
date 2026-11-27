#include "m2c_types.h"
M2C_UNK func_801E4078_59FF88(void *, s32, s32, s32); /* extern */
M2C_UNK func_801F5B04_5B1A14(void *, s32, s32, s32, s32, s32); /* extern */

void func_801DE270_59A180(void *arg0, s16 arg1) {
    if (M2C_FIELD(arg0, u8 *, 0x60) == 2) {
        func_801F5B04_5B1A14(arg0, 6, 0x61, 0x63, 0, 5);
        return;
    }
    func_801E4078_59FF88(arg0, 6, 0x61, 0x63);
}
