#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_080060EC_6FDC7C();                     /* static */

void func_08006098_6FDC28(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0xA4) != 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x78;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080060EC_6FDC7C);
    }
}
