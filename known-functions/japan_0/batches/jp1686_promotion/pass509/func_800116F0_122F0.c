#include "m2c_types.h"
extern void *D_80201534_5BD504;
extern void *D_80201538_5BD508;

void func_800116F0_122F0(void) {
    if ((D_80201534_5BD504 != NULL) && (D_80201538_5BD508 != NULL)) {
        M2C_FIELD(D_80201534_5BD504, u16 *, 0x22) = (u16) (M2C_FIELD(D_80201534_5BD504, u16 *, 0x22) | 0x14);
        M2C_FIELD(D_80201538_5BD508, s8 *, 0x64) = 1;
        M2C_FIELD(D_80201538_5BD508, u8 *, 4) = (u8) (M2C_FIELD(D_80201538_5BD508, u8 *, 4) | 0x80);
    }
}
