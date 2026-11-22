#include "m2c_types.h"
extern char func_80003D40_4940;
extern char func_80034E8C_35A8C;
M2C_UNK func_08002578_701D48();                     /* static */

void func_080024F8_701CC8(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f32) (((f32(*)())&func_80003D40_4940)(M2C_FIELD(arg0, u16 *, 0xD8)) * 20.0f) + M2C_FIELD(arg0, s16 *, 0xD0));
    if (M2C_FIELD(arg1, f32 *, 0x10) > 230.0f) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002578_701D48);
    }
}
