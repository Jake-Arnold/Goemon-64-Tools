#include "m2c_types.h"
void osUnmapTLBAll(void);
typedef struct {
    u8 pad0[0xCF80C];
    u32 unkCF80C[0x20];
} Struct_8015C5C8;

extern Struct_8015C5C8 *D_8015C5C8_15D1C8;

void func_80001FE8_2BE8(void) {
    u32 i;

    i = 0x1F;
    do {
        D_8015C5C8_15D1C8->unkCF80C[i] = 0;
    } while (i-- > 0);
    osUnmapTLBAll();
}
