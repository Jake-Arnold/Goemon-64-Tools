#include "m2c_types.h"
M2C_UNK func_80035A6C_3666C(s32, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_800362D0_36ED0();                      /* extern */
extern s32 D_80072E00_73A00;
extern u16 D_80173290_173E90;

void func_80036454_37054(s32 arg0) {
    if (arg0 != 0) {
        func_800362D0_36ED0();
        D_80173290_173E90 -= 1;
        if (D_80072E00_73A00 != 0) {
            func_80035A6C_3666C(D_80072E00_73A00, 2, 1);
        }
    }
}
