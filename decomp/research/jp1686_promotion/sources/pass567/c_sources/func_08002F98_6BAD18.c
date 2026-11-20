#include "../m2c_types.h"
extern char func_80023CF8_248F8;
extern char func_80034E8C_35A8C;
M2C_UNK func_08002FF4_6BAD74();                     /* static */
extern M2C_UNK D_801624C8_1630C8;

void func_08002F98_6BAD18(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80023CF8_248F8)(0x179);
    M2C_FIELD(arg0, s32 *, 0xE8) = (s32) (M2C_FIELD(arg0, s32 *, 0xE8) | 0x400);
    M2C_FIELD(&D_801624C8_1630C8, s8 *, 0xDC) = 0;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002FF4_6BAD74);
}
