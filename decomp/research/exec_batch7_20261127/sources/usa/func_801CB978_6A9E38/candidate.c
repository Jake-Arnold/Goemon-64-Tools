#include "m2c_types.h"
extern void func_801CB460_6A9920(M2C_UNK *);
extern M2C_UNK D_801CE090_6AC550;
extern u8 D_801CE092_6AC552[];

s32 func_801CB978_6A9E38(u8 arg0) {
    func_801CB460_6A9920(&D_801CE090_6AC550);
    if (D_801CE092_6AC552[arg0 * 4] & 1) {
        return 2;
    }
    return 1;
}
