#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80034E8C_35A8C;
M2C_UNK func_080017D4_706E74();                     /* static */
extern M2C_UNK D_801624C8_1630C8;

void func_0800140C_706AAC(void *arg0) {
    if (M2C_FIELD(&D_801624C8_1630C8, u16 *, 0xDE) == 3) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x200;
        ((M2C_UNK(*)())&func_80023AB0_246B0)(0);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080017D4_706E74);
    }
}
