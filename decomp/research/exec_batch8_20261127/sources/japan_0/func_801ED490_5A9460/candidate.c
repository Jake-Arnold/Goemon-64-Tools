#include "m2c_types.h"

void func_80038838_39438(s32);
void func_801E019C_59C16C(void *, s32);
void func_801E73C8_5A3398(void *);

typedef struct {
    u8 pad0[0x5C];
    u16 unk5C;
} Unk80;

typedef struct {
    u8 pad0[0x80];
    Unk80 *unk80;
} Unk5C;

typedef struct {
    u8 pad0[0x5C];
    Unk5C *unk5C;
} Arg0;

s32 func_801ED490_5A9460(Arg0 *arg0) {
    u16 var_v1;
    Unk80 *temp_v0;

    temp_v0 = arg0->unk5C->unk80;
    var_v1 = (temp_v0 != NULL) ? temp_v0->unk5C : 0;
    if (var_v1 == 0x1A1) {
        func_80038838_39438(0x260);
        func_801E73C8_5A3398(arg0);
        func_801E019C_59C16C(arg0, 0x18);
        return 1;
    }
    return 0;
}
