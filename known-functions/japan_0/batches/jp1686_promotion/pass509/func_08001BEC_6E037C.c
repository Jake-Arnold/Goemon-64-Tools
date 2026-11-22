#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08001C48_6E03D8();                     /* static */

void func_08001BEC_6E037C(void *arg0, M2C_UNK arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x38);
    if (temp_v0 != NULL) {
        if (M2C_FIELD(temp_v0, u8 *, 0x4C) == 0x1D) {
            M2C_FIELD(arg0, s16 *, 0xE0) = 1;
        } else {
            M2C_FIELD(arg0, s16 *, 0xE0) = 0;
        }
    }
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001C48_6E03D8);
}
