#include "m2c_types.h"
s32 func_801D9A58_6044D8(M2C_UNK, M2C_UNK);                  /* extern */
M2C_UNK func_801DBC28_6066A8(s32, M2C_UNK);         /* extern */

void func_801F4584_61F004(s32 arg0) {
    if (func_801D9A58_6044D8(arg0, 0xC25C0000) != 0) {
        func_801DBC28_6066A8(arg0, 0x3E4CCCCD);
        return;
    }
    func_801DBC28_6066A8(arg0, 0xBE4CCCCD);
}
