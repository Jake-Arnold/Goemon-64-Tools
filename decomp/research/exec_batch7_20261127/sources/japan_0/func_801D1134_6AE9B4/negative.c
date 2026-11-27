#include "m2c_types.h"
extern void func_801D0B90_6AE410(M2C_UNK *);
extern M2C_UNK D_801D3850_6B10D0;
extern u8 D_801D3852_6B10D2[];

s32 func_801D1134_6AE9B4(u8 arg0) {
    func_801D0B90_6AE410(&D_801D3850_6B10D0);
    if (D_801D3852_6B10D2[arg0 * 4] & 1) {
        { *(volatile s32 *)0x80000000 = 1; } return 2;
    }
    return 1;
}
