#include "m2c_types.h"
extern char func_80035214_35E14;
extern char func_8003521C_35E1C;
extern char func_80035244_35E44;
extern char func_8021664C_5D1B1C;
extern char func_80219E70_5D5340;
extern M2C_UNK D_8015CC30_15D830;
extern M2C_UNK func_080036EC_737E7C;
extern M2C_UNK func_80218F30_5D4400;
extern M2C_UNK func_8021925C_5D472C;

void func_08003620_737DB0(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x201;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x353;
    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK))&func_80219E70_5D5340)(arg0, 5, 0);
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80035214_35E14)(arg0, &func_8021925C_5D472C);
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80035244_35E44)(arg0, &func_80218F30_5D4400);
    M2C_FIELD(arg0, u8 *, 0x74) = (u8) M2C_FIELD(&D_8015CC30_15D830, u8 *, 0xD8);
    M2C_FIELD(&D_8015CC30_15D830, u8 *, 0xD8) = (u8) (M2C_FIELD(&D_8015CC30_15D830, u8 *, 0xD8) + 1);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 2, 0x3ECCCCCD, 1);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080036EC_737E7C);
}
