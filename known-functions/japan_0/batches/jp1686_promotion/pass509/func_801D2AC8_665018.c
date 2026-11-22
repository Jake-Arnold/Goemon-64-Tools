#include "m2c_types.h"
M2C_UNK func_80011184_11D84(s32, M2C_UNK, s32);     /* extern */
M2C_UNK func_8001119C_11D9C();                      /* extern */
M2C_UNK func_801D1CB8_664208(s32, M2C_UNK *, s32 *); /* extern */

void func_801D2AC8_665018(s32 arg0, s32 arg1) {
    M2C_UNK sp1C;
    s32 sp18;

    func_8001119C_11D9C();
    func_801D1CB8_664208(arg1, &sp1C, &sp18);
    func_80011184_11D84(arg0, -0x10, sp18 / 2);
}
