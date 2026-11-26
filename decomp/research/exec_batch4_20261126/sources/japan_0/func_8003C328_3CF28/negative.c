#include "m2c_types.h"
M2C_UNK func_8003C4D0_3D0D0(void);
extern void *D_80178E00_179A00;

void func_8003C328_3CF28(void) {
    if (M2C_FIELD(D_80178E00_179A00, u8 *, 0x8C) == 0) {
        if (M2C_FIELD(D_80178E00_179A00, u8 *, 0x7C) == 0) {
            M2C_FIELD(D_80178E00_179A00, u8 *, 6) |= 2;
            M2C_FIELD(D_80178E00_179A00, s32 *, 0x28) += M2C_FIELD(D_80178E00_179A00, s32 *, 0x84);
        }
    } else {
        func_8003C4D0_3D0D0();
    }

    *(volatile s32 *)0x80000000 = 1;
}
