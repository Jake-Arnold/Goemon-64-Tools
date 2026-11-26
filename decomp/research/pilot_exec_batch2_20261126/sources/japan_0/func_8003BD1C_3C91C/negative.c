#include "m2c_types.h"
typedef struct {
    u8 pad0[0x93];
    u8 unk_93;
    u8 unk_94;
    u8 pad95[1];
    u16 unk_96;
    s8 unk_98;
    u8 pad99[1];
    u16 unk_9A;
    u16 unk_9C;
    u8 unk_9E;
    u8 unk_9F;
} Unk3BC80_B;
extern Unk3BC80_B *D_80178E00_179A00;

void func_8003BD1C_3C91C(void) {
    D_80178E00_179A00->unk_94 = D_80178E00_179A00->unk_93;
    D_80178E00_179A00->unk_9F = D_80178E00_179A00->unk_9E;
    if (D_80178E00_179A00->unk_9E == 0) {
        D_80178E00_179A00->unk_9C = D_80178E00_179A00->unk_9A;
    } else {
        D_80178E00_179A00->unk_9C = 0;
    }
    D_80178E00_179A00->unk_96 = 0;
    D_80178E00_179A00->unk_98 = D_80178E00_179A00->unk_96;

    *(volatile int *)0x80000000 = 1;
}
