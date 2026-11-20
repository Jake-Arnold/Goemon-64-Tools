#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
f32 func_801D8910_603390(M2C_UNK, M2C_UNK);                  /* extern */
M2C_UNK func_801D8BF0_603670(s32, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801EA9A4_615424();                     /* static */
extern M2C_UNK D_802107C4_63B244;
extern M2C_UNK D_802108F0_63B370;

void func_801EA91C_61539C(void *arg0, s32 arg1) {
    if (func_801D8910_603390(arg0, 0x42700000) == 0.0f) {
        func_80038838_39438(0x235);
        func_801D88EC_60336C(arg0, &D_802108F0_63B370);
        func_801D8BF0_603670(arg1, &D_802107C4_63B244, 0, 0);
        func_80034E8C_35A8C(func_801EA9A4_615424);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x96;
    }
}
