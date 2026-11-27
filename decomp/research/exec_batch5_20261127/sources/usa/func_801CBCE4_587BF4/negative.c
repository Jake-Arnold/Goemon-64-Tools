#include "m2c_types.h"

typedef struct {
    s32 x;
} Unk587BF4;

void func_80013AC4_146C4(Unk587BF4 *);
extern Unk587BF4 D_801FC7B8_5B86C8;

void func_801CBCE4_587BF4(void) {
    Unk587BF4 sp1C = D_801FC7B8_5B86C8;

    func_80013AC4_146C4(&sp1C);

    *(volatile s32 *)0x80000000 = 1;
}
