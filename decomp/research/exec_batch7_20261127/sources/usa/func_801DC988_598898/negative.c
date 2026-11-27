#include "m2c_types.h"

extern u8 D_8020D238_5C9148[1][2];

void func_801DC988_598898(void) {
    s32 i;
    s32 j;

    for (i = 0; i < 1; i++) {
        for (j = 0; j < 2; j++) {
            D_8020D238_5C9148[i][j] = 0;
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
