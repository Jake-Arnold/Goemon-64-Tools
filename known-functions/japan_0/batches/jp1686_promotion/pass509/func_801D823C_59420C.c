#include "m2c_types.h"
s32 func_801D8284_594254();                         /* static */
M2C_UNK func_801D840C_5943DC(void *, s32, u16, s32); /* static */

void func_801D823C_59420C(void *arg0, s32 arg1) {
    if (func_801D8284_594254() == 0) {
        func_801D840C_5943DC(arg0, arg1, M2C_FIELD(arg0, u16 *, 0xCC), ((M2C_FIELD(arg0, u8 *, 0xBC) & 7) << 7) & 0xFFFF);
    }
}
