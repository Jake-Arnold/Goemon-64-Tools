#include "m2c_types.h"
extern char func_80221CCC_5DD19C;

void func_0800105C_6B046C(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x100) {
        ((M2C_UNK(*)())&func_80221CCC_5DD19C)();
        return;
    }
    M2C_FIELD(arg1, u16 *, 0x7E) = (u16) M2C_FIELD(arg0, u16 *, 0xA8);
}
