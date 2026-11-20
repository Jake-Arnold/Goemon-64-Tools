#include "m2c_types.h"
extern char func_80226A3C_5E1FCC;

void func_08001048_6B4F48(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x100) {
        ((M2C_UNK(*)())&func_80226A3C_5E1FCC)();
        return;
    }
    M2C_FIELD(arg1, u16 *, 0x7E) = (u16) M2C_FIELD(arg0, u16 *, 0xA8);
}
