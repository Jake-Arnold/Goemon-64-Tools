#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021DF60_5D9430;
M2C_UNK func_080029CC_703ACC(void *);               /* static */
M2C_UNK func_0800316C_70426C();                     /* static */

void func_080030B0_7041B0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s16 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s16 *, 0xDE);
    M2C_FIELD(arg0, s16 *, 0xDA) = (s16) (M2C_FIELD(arg0, s16 *, 0xDA) - M2C_FIELD(arg0, s16 *, 0xDC));
    if (temp_v0 > 0) {
        M2C_FIELD(arg0, s16 *, 0xDE) = (s16) (temp_v0 - 3);
    } else {
        M2C_FIELD(arg0, s16 *, 0xDE) = 0;
    }
    ((M2C_UNK(*)())&func_8021DF60_5D9430)(arg0, M2C_FIELD(arg0, s16 *, 0xDE), 0xFF, 0xFF, 0);
    if (M2C_FIELD(arg0, s16 *, 0xDA) == 0) {
        M2C_FIELD(arg0, s16 *, 0xDC) = (s16) -M2C_FIELD(arg0, s16 *, 0xDC);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x50;
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~1);
        M2C_FIELD(arg0, s16 *, 0xD4) = 0;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800316C_70426C);
    }
    func_080029CC_703ACC(arg0);
}
