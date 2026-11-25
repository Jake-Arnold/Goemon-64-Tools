#include "m2c_types.h"
extern char func_80012380_12F80;
extern char func_800124A0_130A0;
extern char func_80012518_13118;
extern char func_80012628_13228;
extern char func_8003521C_35E1C;
M2C_UNK func_08000644_726AD4();                     /* static */

void func_0800057C_726A0C(void *arg0, M2C_UNK arg1) {
    void *temp_s0;

    temp_s0 = M2C_FIELD(arg0, void **, 0xD0);
    if (M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
        ((M2C_UNK(*)())&func_800124A0_130A0)(M2C_FIELD(temp_s0, s32 *, 0x18), 0x42480000);
        ((M2C_UNK(*)())&func_80012518_13118)(M2C_FIELD(temp_s0, s32 *, 0x18), 0xC1100000, 0x43A20000, 0x43770000);
        ((M2C_UNK(*)())&func_80012628_13228)(M2C_FIELD(temp_s0, s32 *, 0x18), 0xC0000000, 0x43968000, 0x43A10000);
    }
    if (((s32(*)())&func_80012380_12F80)(M2C_FIELD(temp_s0, s32 *, 0x18)) == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 0U;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000644_726AD4);
        return;
    }
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (M2C_FIELD(arg0, u16 *, 0x8A) + 1);
}
