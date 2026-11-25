#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_080061C8_6F96A8();                     /* static */

void func_08006174_6F9654(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0xA4) != 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x78;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080061C8_6F96A8);
    }
}
