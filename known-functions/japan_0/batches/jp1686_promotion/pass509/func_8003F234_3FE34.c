#include "m2c_types.h"
extern s32 D_801CCE80_1CDA80;
extern void *D_80201518;

void func_8003F234_3FE34(void) {
    if (D_80201518 != NULL) {
        D_801CCE80_1CDA80 = (s32) M2C_FIELD(D_80201518, u8 *, 0x60);
        return;
    }
    D_801CCE80_1CDA80 = -1;
}
