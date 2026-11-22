#include "m2c_types.h"
extern void *D_80201534_5BD504;
extern void *D_80201538_5BD508;

void func_80011744_12344(void) {
    if ((D_80201534_5BD504 != NULL) && (D_80201538_5BD508 != NULL)) {
        M2C_FIELD(D_80201534_5BD504, u16 *, 0x22) = (u16) (M2C_FIELD(D_80201534_5BD504, u16 *, 0x22) & 0xFFEB);
        M2C_FIELD(D_80201538_5BD508, s8 *, 0x64) = 0;
        M2C_FIELD(D_80201538_5BD508, u8 *, 4) = (u8) (M2C_FIELD(D_80201538_5BD508, u8 *, 4) & 0xFF7F);
    }
}
