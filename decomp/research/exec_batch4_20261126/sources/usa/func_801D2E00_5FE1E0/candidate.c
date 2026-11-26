#include "m2c_types.h"

typedef struct {
    u8 pad0[0x140];
    u8 unk140[0x11];
} Struct801D2E00;

extern Struct801D2E00 *D_8020EED0_63A2B0;

s32 func_801D2E00_5FE1E0(void) {
    s32 var_v1;
    u8 *temp_v0;

    var_v1 = 0;
    temp_v0 = D_8020EED0_63A2B0->unk140;
    if (temp_v0[8] != 0) {
        var_v1 = 1;
    }
    if (temp_v0[9] != 0) {
        var_v1 |= 2;
    }
    if (temp_v0[0xA] != 0) {
        var_v1 |= 4;
    }
    if (temp_v0[0xB] != 0) {
        var_v1 |= 8;
    }
    if (temp_v0[0xC] != 0) {
        var_v1 |= 0x10;
    }
    if (temp_v0[0xE] != 0) {
        var_v1 |= 0x20;
    }
    if (temp_v0[0xF] != 0) {
        var_v1 |= 0x40;
    }
    if (temp_v0[0x10] != 0) {
        var_v1 |= 0x80;
    }
    return var_v1;
}
