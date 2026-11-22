#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80222CD0_5DE260;
M2C_UNK func_080029B0_708050(void *);               /* static */
M2C_UNK func_08003038_7086D8();                     /* static */

void func_08002F70_708610(void *arg0, M2C_UNK arg1) {
    s16 temp_v0;
    s16 temp_v0_2;

    temp_v0 = M2C_FIELD(arg0, s16 *, 0xDE);
    M2C_FIELD(arg0, s16 *, 0xD4) = 0;
    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~1);
    if (temp_v0 < 0xFF) {
        M2C_FIELD(arg0, s16 *, 0xDE) = (s16) (temp_v0 + 3);
    } else {
        M2C_FIELD(arg0, s16 *, 0xDE) = 0xFF;
    }
    ((M2C_UNK(*)())&func_80222CD0_5DE260)(arg0, M2C_FIELD(arg0, s16 *, 0xDE), 0xFF, 0xFF, 0);
    M2C_FIELD(arg0, s16 *, 0xDA) = (s16) (M2C_FIELD(arg0, s16 *, 0xDC) + M2C_FIELD(arg0, s16 *, 0xDA));
    temp_v0_2 = M2C_FIELD(arg0, s16 *, 0xDA);
    if ((temp_v0_2 >= 0x41) || (temp_v0_2 < -0x40)) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x80;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003038_7086D8);
    }
    func_080029B0_708050(arg0);
}
