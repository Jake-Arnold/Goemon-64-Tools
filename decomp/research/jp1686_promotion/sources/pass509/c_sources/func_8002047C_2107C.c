#include "m2c_types.h"
M2C_UNK func_8000359C_419C();                       /* extern */
M2C_UNK func_80004170_4D70();                       /* extern */
M2C_UNK func_800041DC_4DDC(M2C_UNK, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK osViBlack(M2C_UNK);                         /* extern */
extern s32 D_80072A98_73698;
extern M2C_UNK D_80081470_82070;
extern s32 D_80161DCC_1629CC;

void func_8002047C_2107C(void) {
    osViBlack(0);
    func_80004170_4D70();
    D_80072A98_73698 = D_80161DCC_1629CC;
    func_800041DC_4DDC(0, &D_80081470_82070, 0x70, 0x30);
    func_8000359C_419C();
}
