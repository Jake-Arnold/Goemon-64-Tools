#include "../m2c_types.h"
void func_80215480_69CB80(void *arg0, s32 arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(temp_v0, s32 *, 0x50) = (s32) (M2C_FIELD(temp_v0, s32 *, 0x38) + arg1 + 0xF8000000);
}
