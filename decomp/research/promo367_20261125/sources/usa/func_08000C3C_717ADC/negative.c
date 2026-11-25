#include "../m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_080001DC_71707C();                     /* static */
M2C_UNK func_080028B4_719754(void *);               /* static */
M2C_UNK func_08002C30_719AD0();                     /* static */

void func_08000C3C_717ADC(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~0x4000);
    func_08002C30_719AD0();
    func_080028B4_719754(arg0);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080001DC_71707C);
}
