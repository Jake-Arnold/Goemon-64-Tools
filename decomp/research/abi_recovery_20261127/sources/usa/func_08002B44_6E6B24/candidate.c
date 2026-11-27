#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80219330_5D4800;
extern char func_8021B09C_5D656C;
extern M2C_UNK func_08002BE0_6E6BC0;

void func_08002B44_6E6B24(void *arg0, void *arg1) {
    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 0, 1);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0x3EAAAAAB, 1);
    ((M2C_UNK (*)(void *, u8, u8, u8, s32, s32))&func_80219330_5D4800)(arg0, M2C_FIELD(arg0, u8 *, 0xE8), M2C_FIELD(arg0, u8 *, 0xE9), M2C_FIELD(arg0, u8 *, 0xEA), M2C_FIELD(arg0, u8 *, 0xEB) * 4, (s32) M2C_FIELD(arg1, u16 *, 0x16));
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08002BE0_6E6BC0);
}
