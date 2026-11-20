#include "m2c_types.h"
extern s32 D_801CCE80_1CDA80;
extern void *D_80201514_5BD4E4;

void func_8003F200_3FE00(void) {
    if (D_80201514_5BD4E4 != NULL) {
        D_801CCE80_1CDA80 = (s32) M2C_FIELD(D_80201514_5BD4E4, u8 *, 0x60);
        return;
    }
    D_801CCE80_1CDA80 = -1;
}
