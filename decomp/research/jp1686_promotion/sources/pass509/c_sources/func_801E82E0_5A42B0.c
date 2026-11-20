#include "m2c_types.h"
M2C_UNK func_801E2A90_59EA60(void *, M2C_UNK);      /* extern */
M2C_UNK func_801E832C_5A42FC();                     /* static */

void func_801E82E0_5A42B0(void *arg0) {
    func_801E832C_5A42FC();
    if (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x59) != 0) {
        func_801E2A90_59EA60(arg0, 7);
        return;
    }
    func_801E2A90_59EA60(arg0, 0x26);
}
