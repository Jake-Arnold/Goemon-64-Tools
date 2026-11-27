#include "m2c_types.h"
M2C_UNK func_08000000_6FB200(void *, u8);                   /* extern */
extern char func_8003521C_35E1C;
extern char func_802239B0_5DEE80;
extern M2C_UNK func_08000234_6FB434;

void func_080002A0_6FB4A0(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x220;
    func_08000000_6FB200(arg0, M2C_FIELD(arg0, u8 *, 0xD5));
    ((M2C_UNK (*)(void *, s32, s32, u8, s32))&func_802239B0_5DEE80)(arg0, (M2C_FIELD(arg0, u8 *, 0xD0) * 4) & 0xFFFF, (M2C_FIELD(arg0, u8 *, 0xD1) * 4) & 0xFFFF, M2C_FIELD(arg0, u8 *, 0xD2), (s32) M2C_FIELD(arg0, u8 *, 0xD3));
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08000234_6FB434);

    *(volatile s32 *)0x80000000 = 1;
}
