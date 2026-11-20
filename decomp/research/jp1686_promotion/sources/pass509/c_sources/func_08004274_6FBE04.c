#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_080042E8_6FBE78();                     /* static */
extern M2C_UNK D_801624C8_1630C8;

void func_08004274_6FBE04(void *arg0, M2C_UNK arg1) {
    if ((s32) M2C_FIELD(&D_801624C8_1630C8, u8 *, 0x90) >= 6) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x15E, arg0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x78;
        M2C_FIELD(arg0, f32 *, 0x7C) = -0.5f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080042E8_6FBE78, arg0);
    }
}
