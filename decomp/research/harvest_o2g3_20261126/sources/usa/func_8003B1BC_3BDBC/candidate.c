#include "m2c_types.h"
M2C_UNK func_8003AFB0_3BBB0();                      /* extern */
M2C_UNK func_8003B248_3BE48();                      /* extern */
extern void *D_801C1728_1C2328;

void func_8003B1BC_3BDBC(void) {
    M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4C) = 0U;
    if (M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4E) != 0) {
        M2C_FIELD(D_801C1728_1C2328, s16 *, 0x4A) = 0x20;
        func_8003AFB0_3BBB0();
        M2C_FIELD(D_801C1728_1C2328, s8 *, 0x49) = 0;
        M2C_FIELD(D_801C1728_1C2328, s16 *, 0x4A) = 0x100;
        M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4C) = (u16) M2C_FIELD(D_801C1728_1C2328, u16 *, 0x4E);
        func_8003AFB0_3BBB0();
        return;
    }
    M2C_FIELD(D_801C1728_1C2328, s16 *, 0x4A) = 0x100;
    func_8003AFB0_3BBB0();
    func_8003B248_3BE48();
}
