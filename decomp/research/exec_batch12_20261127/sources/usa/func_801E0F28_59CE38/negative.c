#include "m2c_types.h"

typedef struct {
    u8 pad0[0x60];
    u8 unk60;
} Struct_1E0F28;

typedef struct {
    u8 unk0;
    u8 pad1[3];
} Struct_802043A0;

void func_801E7B24_5A3A34(Struct_1E0F28 *, s32, u8);
void func_801E83F8_5A4308(Struct_1E0F28 *);
extern Struct_802043A0 D_802043A0_5C02B0[];

void func_801E0F28_59CE38(Struct_1E0F28 *arg0, s32 arg1) {
    u8 temp_v0;

    func_801E7B24_5A3A34(arg0, 2, D_802043A0_5C02B0[arg0->unk60].unk0);
    temp_v0 = arg0->unk60;
    if (temp_v0 == 1 || temp_v0 == 2) {
        func_801E83F8_5A4308(arg0);
    }

    *(volatile int *)0x80000000 = 1;
}
