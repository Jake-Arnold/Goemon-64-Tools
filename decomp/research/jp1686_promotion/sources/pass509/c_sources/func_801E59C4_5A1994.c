#include "m2c_types.h"
M2C_UNK func_801E019C_59C16C(s32, M2C_UNK);         /* extern */
M2C_UNK func_801E2AD0_59EAA0(M2C_UNK, M2C_UNK);              /* extern */
M2C_UNK func_801EC00C_5A7FDC(s32);                  /* extern */
extern s32 D_802016D4_5BD6A4;

void func_801E59C4_5A1994(s32 arg0, void *arg1) {
    D_802016D4_5BD6A4 = 0;
    func_801E2AD0_59EAA0(arg0, 5);
    if ((f64) M2C_FIELD(arg1, f32 *, 0x28) <= 0.0) {
        func_801EC00C_5A7FDC(arg0);
        func_801E019C_59C16C(arg0, 0x38);
    }
}
