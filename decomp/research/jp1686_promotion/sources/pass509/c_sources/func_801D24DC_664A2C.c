#include "m2c_types.h"
M2C_UNK func_801D23F8_664948();                     /* static */
extern s32 D_801E8E24_67B374;
extern s32 D_801E8E40_67B390;

void func_801D24DC_664A2C(void) {
    func_801D23F8_664948();
    if (D_801E8E40_67B390 & 0x800) {
        D_801E8E24_67B374 = 0;
    }
    if (D_801E8E40_67B390 & 0x400) {
        D_801E8E24_67B374 = 1;
    }
}
