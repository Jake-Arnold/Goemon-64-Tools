#include "m2c_types.h"
M2C_UNK func_08000000_6FF7D0(void *, u8);                   /* extern */
extern char func_80034E8C_35A8C;
extern char func_80228720_5E3CB0;
extern M2C_UNK func_08000234_6FFA04;

void func_080002A0_6FFA70(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x220;
    func_08000000_6FF7D0(arg0, M2C_FIELD(arg0, u8 *, 0xD5));
    ((M2C_UNK (*)(void *, s32, s32, u8, s32))&func_80228720_5E3CB0)(arg0, (M2C_FIELD(arg0, u8 *, 0xD0) * 4) & 0xFFFF, (M2C_FIELD(arg0, u8 *, 0xD1) * 4) & 0xFFFF, M2C_FIELD(arg0, u8 *, 0xD2), (s32) M2C_FIELD(arg0, u8 *, 0xD3));
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08000234_6FFA04);
}
