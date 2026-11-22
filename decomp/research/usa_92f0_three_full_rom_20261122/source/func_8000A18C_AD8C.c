#include "common.h"

/* Offsets are original machine-code data offsets, not invented field semantics. */
typedef struct {
    u8 pad[0x5D06];
    s16 field_5D06;
    s16 field_5D08;
    s16 field_5D0A;
    s16 field_5D0C;
    s32 field_5D10;
} File92State;

extern File92State D_8014CCC0_14D8C0;

void func_8000A18C_AD8C(void) {
    D_8014CCC0_14D8C0.field_5D0C = 255;
    D_8014CCC0_14D8C0.field_5D10 = 0;
    D_8014CCC0_14D8C0.field_5D0A = D_8014CCC0_14D8C0.field_5D0C;
    D_8014CCC0_14D8C0.field_5D08 = D_8014CCC0_14D8C0.field_5D0A;
    D_8014CCC0_14D8C0.field_5D06 = D_8014CCC0_14D8C0.field_5D08;
}
