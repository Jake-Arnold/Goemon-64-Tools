#include "probe_common.h"
extern void *D_8016DAB4_16E6B4;

void func_80035344_35F44(void) {
    M2C_FIELD(D_8016DAB4_16E6B4, M2C_UNK (**)(void *, s32), 0xC) = (M2C_UNK (*)(void *, s32)) M2C_FIELD(D_8016DAB4_16E6B4, M2C_UNK (**)(void *, s32), 0x14);
    M2C_FIELD(D_8016DAB4_16E6B4, M2C_UNK (**)(void *, s32), 0xC)(D_8016DAB4_16E6B4, M2C_FIELD(D_8016DAB4_16E6B4, s32 *, 0x18));
}
