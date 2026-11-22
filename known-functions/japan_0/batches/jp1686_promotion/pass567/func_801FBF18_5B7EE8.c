#include "../m2c_types.h"
M2C_UNK func_801ED278_5A9248();                     /* extern */

void func_801FBF18_5B7EE8(void *arg0) {
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x86) = 0;
    M2C_FIELD(arg0, s8 *, 0x61) = 0;
    M2C_FIELD(arg0, s16 *, 0x40) = 0;
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) | 1);
    func_801ED278_5A9248();
}
