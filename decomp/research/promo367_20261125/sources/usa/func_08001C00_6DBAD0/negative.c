#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08001C5C_6DBB2C();                     /* static */

void func_08001C00_6DBAD0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x38);
    if (temp_v0 != NULL) {
        if (M2C_FIELD(temp_v0, u8 *, 0x4C) == 0x1D) {
            M2C_FIELD(arg0, s16 *, 0xE0) = 1;
        } else {
            M2C_FIELD(arg0, s16 *, 0xE0) = 0;
        }
    }
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001C5C_6DBB2C);
}
