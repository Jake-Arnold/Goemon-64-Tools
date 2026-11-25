#include "m2c_types.h"
extern char func_80024088_24C88;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_800370E8_37CE8;
extern char func_800371B4_37DB4;
extern char func_80221CCC_5DD19C;
extern u16 D_800C7AB4;
extern M2C_UNK func_800354B4_360B4;

void func_08001568_6B0978(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x100) {
        ((M2C_UNK(*)())&func_80221CCC_5DD19C)();
    } else {
        M2C_FIELD(arg1, u16 *, 0x7E) = (u16) M2C_FIELD(arg0, u16 *, 0xA8);
    }
    if (((s32(*)())&func_800240DC_24CDC)(0x79) != 0) {
        ((M2C_UNK(*)())&func_80024088_24C88)(0x79);
        if (D_800C7AB4 == 0x3F) {
            ((M2C_UNK(*)())&func_800370E8_37CE8)();
        } else {
            ((M2C_UNK(*)())&func_800371B4_37DB4)();
        }
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_800354B4_360B4);
    }
}
