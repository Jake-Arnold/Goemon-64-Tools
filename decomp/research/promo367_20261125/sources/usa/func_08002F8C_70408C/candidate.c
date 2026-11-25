#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021DF60_5D9430;
M2C_UNK func_080029CC_703ACC(void *);               /* static */
M2C_UNK func_08003054_704154();                     /* static */

void func_08002F8C_70408C(void *arg0, M2C_UNK arg1) {
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
    ((M2C_UNK(*)())&func_8021DF60_5D9430)(arg0, M2C_FIELD(arg0, s16 *, 0xDE), 0xFF, 0xFF, 0);
    M2C_FIELD(arg0, s16 *, 0xDA) = (s16) (M2C_FIELD(arg0, s16 *, 0xDC) + M2C_FIELD(arg0, s16 *, 0xDA));
    temp_v0_2 = M2C_FIELD(arg0, s16 *, 0xDA);
    if ((temp_v0_2 >= 0x41) || (temp_v0_2 < -0x40)) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x80;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08003054_704154);
    }
    func_080029CC_703ACC(arg0);
}
