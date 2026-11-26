#include "m2c_types.h"
typedef struct {
    u8 pad[0x6C];
    s32 unk_6C;
} Unk3BC80;
extern Unk3BC80 *D_80178E00_179A00;
extern s32 D_80178E04_179A04;

void func_8003C7B8_3D3B8(void) {
    D_80178E04_179A04 = D_80178E00_179A00->unk_6C;

    *(volatile int *)0x80000000 = 1;
}
