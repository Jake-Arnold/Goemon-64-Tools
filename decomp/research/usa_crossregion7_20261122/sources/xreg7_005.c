#include "probe_common.h"
M2C_UNK func_801E8560_5A4470(f32, f32, s32);        /* static */

void func_801E864C_5A455C(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    func_801E8560_5A4470(M2C_FIELD(temp_v0, f32 *, 8), M2C_FIELD(temp_v0, f32 *, 0xC), M2C_FIELD(temp_v0, s32 *, 0x10));
}
