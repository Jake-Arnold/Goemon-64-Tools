#include "m2c_types.h"
void *func_80034A78_35678(void *, s32, s32);
s32 func_80035B5C_3675C(void *, s32, s32);
M2C_UNK func_801F34C8_5AF498(void *, void *, u8);
extern s32 D_80209758_5C5728[];

void func_801F5948_5B1918(void *arg0, u8 arg1) {
    void *temp_v0;

    temp_v0 = func_80034A78_35678(arg0, D_80209758_5C5728[arg1], 0);
    if (temp_v0 != NULL) {
        func_801F34C8_5AF498(temp_v0, arg0, arg1);
        if (func_80035B5C_3675C(temp_v0, 2, 3) == 0) {
            M2C_FIELD(temp_v0, s8 *, 0x65) = 1;
        }
    }
}
