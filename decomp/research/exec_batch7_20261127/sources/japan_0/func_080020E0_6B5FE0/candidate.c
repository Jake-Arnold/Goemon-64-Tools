#include "m2c_types.h"
extern void func_80034E8C_35A8C(void *);
extern M2C_UNK func_08002130_6B6030;

void func_080020E0_6B5FE0(void *arg0, M2C_UNK arg1) {
    void (*fn)(void *) = func_80034E8C_35A8C;
    if (M2C_FIELD(arg0, s32 *, 0xE0)++ < 10) {
        M2C_FIELD(arg0, s32 *, 0xE0)++;
    } else {
        fn(&func_08002130_6B6030);
    }
}
