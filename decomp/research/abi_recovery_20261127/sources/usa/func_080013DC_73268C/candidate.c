#include "m2c_types.h"
extern char func_80035214_35E14;
extern char func_8003521C_35E1C;
extern char func_80035244_35E44;
extern char func_8021664C_5D1B1C;
extern char func_80218D90_5D4260;
extern char func_80219E70_5D5340;
extern M2C_UNK D_8015CC30_15D830;
extern M2C_UNK func_080014E4_732794;
extern M2C_UNK func_80218F30_5D4400;
extern M2C_UNK func_8021925C_5D472C;

void func_080013DC_73268C(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x02800301;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x2E1;
    M2C_FIELD(arg0, s8 *, 0x75) = 0;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x355;
    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK))&func_80219E70_5D5340)(arg0, 8, 0xA);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_80218D90_5D4260)(arg0, 5, 5, 5, -5);
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80035214_35E14)(arg0, &func_8021925C_5D472C);
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80035244_35E44)(arg0, &func_80218F30_5D4400);
    M2C_FIELD(arg0, u8 *, 0x74) = (u8) M2C_FIELD(&D_8015CC30_15D830, u8 *, 0xD8);
    M2C_FIELD(&D_8015CC30_15D830, u8 *, 0xD8) = (u8) (M2C_FIELD(&D_8015CC30_15D830, u8 *, 0xD8) + 1);
    M2C_FIELD(arg0, s16 *, 0xA8) = 0x2A;
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0x3E2AAAAB, 1);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080014E4_732794);
}
