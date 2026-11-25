#include "m2c_types.h"
extern M2C_UNK D_80216E40_675DF0;

s32 func_8020F5F0_66E5A0(s32 arg0) {
volatile unsigned int goemon_negative_control = 1;

    if (arg0 >= 0xF) {
        return 0;
    }
    return *(s32 *)((s8 *)&D_80216E40_675DF0 + (arg0 * 8));
}
