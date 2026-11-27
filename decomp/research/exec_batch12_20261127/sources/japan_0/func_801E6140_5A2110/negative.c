#include "m2c_types.h"

typedef struct {
    u8 pad0[0x60];
    u8 unk60;
} Struct_1E0F28;

typedef struct {
    u8 unk0;
    u8 pad1[3];
} Struct_802043A0;

void func_801ECC4C_5A8C1C(Struct_1E0F28 *, s32, u8);
void func_801ED4F8_5A94C8(Struct_1E0F28 *);
extern Struct_802043A0 D_80209290_5C5260[];

void func_801E6140_5A2110(Struct_1E0F28 *arg0, s32 arg1) {
    u8 temp_v0;

    func_801ECC4C_5A8C1C(arg0, 2, D_80209290_5C5260[arg0->unk60].unk0);
    temp_v0 = arg0->unk60;
    if (temp_v0 == 1 || temp_v0 == 2) {
        func_801ED4F8_5A94C8(arg0);
    }

    *(volatile int *)0x80000000 = 1;
}
