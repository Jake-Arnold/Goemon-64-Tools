#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
extern M2C_UNK func_080008E8_711638;
extern M2C_UNK func_08000A8C_7117DC;

void func_08000854_7115A4(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
    if (((s32(*)())&func_80023B54_24754)(M2C_FIELD(arg0, u16 *, 0xD0), arg0) != 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_080008E8_711638, arg0);
        return;
    }
    M2C_FIELD(arg0, M2C_UNK **, 0xBC) = &func_080008E8_711638;
    ((M2C_UNK(*)())&func_80023AB0_246B0)(M2C_FIELD(arg0, u16 *, 0xD0), arg0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08000A8C_7117DC);
}
