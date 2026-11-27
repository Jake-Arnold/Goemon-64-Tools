#include "m2c_types.h"
void func_802092F0_633D70(void *, u8);

void func_8020576C_6301EC(void *arg0, u8 arg1) {
    M2C_FIELD(arg0, s32 *, 0xB4)++;
    if (M2C_FIELD(arg0, s32 *, 0xB4) >= 3) {
        M2C_FIELD(arg0, s32 *, 0xB4) = 0;
    }
    func_802092F0_633D70(arg0, (u8)(M2C_FIELD(arg0, s32 *, 0xB4) + arg1));
}
