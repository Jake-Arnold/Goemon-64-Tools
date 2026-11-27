#include "m2c_types.h"
M2C_UNK func_8000F1E0_FDE0(u16, M2C_UNK *, void *, f32);
extern M2C_UNK D_802119E0_5CD9B0;

void func_8021F850_5DADE0(void *arg0, u16 arg1) {
    void *tmp = M2C_FIELD(arg0, void **, 0x18);
    func_8000F1E0_FDE0(arg1, &D_802119E0_5CD9B0, tmp, 400.0f);

    *(volatile s32 *)0x80000000 = 1;
}
