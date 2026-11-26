#include "m2c_types.h"
typedef struct {
    u8 pad[0xC];
    u8 unk_C;
} Unk3BC80_C;
extern Unk3BC80_C *D_80178E00_179A00;
extern u8 *D_80178E04_179A04;

void func_8003C93C_3D53C(void) {
    D_80178E00_179A00->unk_C = *D_80178E04_179A04;
    D_80178E04_179A04++;

    *(volatile int *)0x80000000 = 1;
}
