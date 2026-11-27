#include "m2c_types.h"
M2C_UNK func_08000000_6D5F50();                     /* extern */
extern char func_8003521C_35E1C;
extern char func_802196FC_5D4BCC;
extern M2C_UNK func_08000634_6D6584;

void func_08000598_6D64E8(void *arg0, M2C_UNK arg1) {
    func_08000000_6D5F50();
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x200000);
    if ((((s32  (*)(void *, f32, f32, f32, s32))&func_802196FC_5D4BCC)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), 0.0f, (f32) M2C_FIELD(arg0, s16 *, 0xA2), 8) == 0) && !(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08000634_6D6584);
    }

    *(volatile s32 *)0x80000000 = 1;
}
