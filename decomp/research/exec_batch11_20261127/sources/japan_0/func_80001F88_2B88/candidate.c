#include "m2c_types.h"
void osUnmapTLBAll(void);
typedef struct {
    u8 pad0[0xCF80C];
    u32 unkCF80C[0x20];
} Struct_8015C5C8;

extern Struct_8015C5C8 *g_system_ptr;

void func_80001F88_2B88(void) {
    u32 i;

    i = 0x1F;
    do {
        g_system_ptr->unkCF80C[i] = 0;
    } while (i-- > 0);
    osUnmapTLBAll();
}
