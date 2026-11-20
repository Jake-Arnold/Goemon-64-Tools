#include "m2c_types.h"
s32 func_8000FFF0_10BF0(M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK *, s32); /* extern */
M2C_UNK func_800134D0_140D0();                      /* extern */
M2C_UNK func_80013654_14254(M2C_UNK *);             /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK osViSetSpecialFeatures(M2C_UNK);            /* extern */
extern M2C_UNK D_8012C00;
extern M2C_UNK D_801D8FB8_66B508;
extern s32 D_801E8E50_67B3A0;
extern s32 D_801E8E54_67B3A4;
extern M2C_UNK func_08000000_6B10D0;

void func_801D5440_667990(void) {
    osViSetSpecialFeatures(0x40);
    func_800134D0_140D0();
    func_80038838_39438(1);
    func_80013654_14254(&D_801D8FB8_66B508);
    D_801E8E50_67B3A0 = func_8000FFF0_10BF0(0xA0, 0xF0, 0x10, 0, &func_08000000_6B10D0, 0x4CE);
    D_801E8E54_67B3A4 = func_8000FFF0_10BF0(0xA0, 0xF0, 0x10, 0, &D_8012C00, 0x4CE);
}
