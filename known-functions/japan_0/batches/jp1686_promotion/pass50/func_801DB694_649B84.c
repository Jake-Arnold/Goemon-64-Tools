#include "m2c_types.h"
M2C_UNK func_801DC010_64A500();                     /* static */

void func_801DB694_649B84(void *arg0) {
    s16 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s16 *, 0xB8) + M2C_FIELD(arg0, s16 *, 0xBA);
    M2C_FIELD(arg0, s16 *, 0xB8) = temp_v0;
    if (temp_v0 >= 0x80) {
        M2C_FIELD(arg0, s8 *, 0xA0) = 2;
    }
    func_801DC010_64A500();
}
