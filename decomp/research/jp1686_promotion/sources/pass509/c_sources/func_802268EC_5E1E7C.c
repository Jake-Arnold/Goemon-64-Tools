#include "m2c_types.h"
extern s32 D_80201514_5BD4E4;
extern s32 D_80201518;

s32 func_802268EC_5E1E7C(void *arg0) {
    s32 temp_v0;
    s32 temp_v1;
    s32 var_a2;
    u8 temp_v0_2;
    void *temp_a1;

    temp_v1 = M2C_FIELD(arg0, s32 *, 0x68);
    if (temp_v1 & 0x100) {
        temp_v0 = M2C_FIELD(arg0, s32 *, 0x34);
        M2C_FIELD(arg0, s32 *, 0xEC) = temp_v0;
        if (temp_v0 != D_80201514_5BD4E4) {
            return 0;
        }
        return M2C_FIELD(arg0, s32 *, 0xEC);
    }
    temp_a1 = M2C_FIELD(arg0, void **, 0x18);
    temp_v0_2 = M2C_FIELD(temp_a1, u8 *, 0x7C);
    if (temp_v0_2 & 8) {
        if (!(temp_v0_2 & 0x10)) {
            var_a2 = D_80201514_5BD4E4;
        } else {
            var_a2 = D_80201518;
        }
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v1 | 0x100);
        M2C_FIELD(arg0, s32 *, 0xEC) = var_a2;
        M2C_FIELD(temp_a1, u8 *, 0x7C) = (u8) (M2C_FIELD(temp_a1, u8 *, 0x7C) & 0xFFE7);
        return M2C_FIELD(arg0, s32 *, 0xEC);
    }
    return 0;
}
