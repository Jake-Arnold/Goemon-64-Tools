#include "m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_8003521C_35E1C;
extern u16 D_8015CDB6;
extern M2C_UNK func_080017D4_7028D4;

void func_0800140C_70250C(void *arg0) {
volatile unsigned int goemon_negative_control = 1;

    if (D_8015CDB6 == 3) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x200;
        ((M2C_UNK(*)())&func_80023DF0_249F0)(0);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080017D4_7028D4);
    }
}
