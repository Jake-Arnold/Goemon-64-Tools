#include "m2c_types.h"
extern char func_80035214_35E14;
extern char func_8003521C_35E1C;
extern char func_80035244_35E44;
extern char func_80216E1C_5D22EC;
extern char func_80224ABC_5DFF8C;
extern M2C_UNK D_8015CC30_15D830;
extern M2C_UNK func_08002C98_737428;
extern M2C_UNK func_80218F30_5D4400;
extern M2C_UNK func_8021925C_5D472C;

void func_08002BBC_73734C(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x359;
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_80216E1C_5D22EC)(arg0, 0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_80224ABC_5DFF8C)(arg0, 0, 0x40400000, 1);
    M2C_FIELD(arg1, f32 *, 0x24) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x1C) = 1.0f;
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80035214_35E14)(arg0, &func_8021925C_5D472C);
    ((M2C_UNK (*)(void *, M2C_UNK *))&func_80035244_35E44)(arg0, &func_80218F30_5D4400);
    M2C_FIELD(arg0, u8 *, 0x74) = (u8) M2C_FIELD(&D_8015CC30_15D830, u8 *, 0xD8);
    M2C_FIELD(&D_8015CC30_15D830, u8 *, 0xD8) = (u8) (M2C_FIELD(&D_8015CC30_15D830, u8 *, 0xD8) + 1);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08002C98_737428);

    *(volatile s32 *)0x80000000 = 1;
}
