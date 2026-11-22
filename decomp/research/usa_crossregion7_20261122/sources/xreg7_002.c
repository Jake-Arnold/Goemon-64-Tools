#include "probe_common.h"
void func_801D0B1C_63F96C(void *arg0, void *arg1) {
    s16 var_v1;
    u32 var_v0;
    M2C_FIELD(arg1, s32 *, 0x318) = (s32)(M2C_FIELD(arg1, s32 *, 0x318) - M2C_FIELD(arg0, s32 *, 0xAC));
    var_v0 = M2C_FIELD(arg1, s32 *, 0x354) + M2C_FIELD(arg1, u32 *, 0x350);
    M2C_FIELD(arg1, u32 *, 0x350) = var_v0;
    var_v1 = M2C_FIELD(arg0, s8 *, 0xA2) - 1;
    if (var_v1 == 0) {
        M2C_FIELD(arg0, s8 *, 0x9D) = 2;
        var_v0 = 0;
        var_v1 = 0xA;
        M2C_FIELD(arg1, s16 *, 0) = (s16)(M2C_FIELD(arg1, s16 *, 0) | 2);
    }
    M2C_FIELD(arg0, s8 *, 0xA2) = (s8)var_v1;
    M2C_FIELD(arg1, s16 *, 0x358) = (s16)(var_v0 >> 0x14);
}
