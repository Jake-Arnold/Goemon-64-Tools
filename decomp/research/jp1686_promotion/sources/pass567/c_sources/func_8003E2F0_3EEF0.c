#include "../m2c_types.h"
M2C_UNK func_8000C568_D168();                       /* extern */
M2C_UNK func_8003D098_3DC98();                      /* extern */
extern s32 D_8007D28C_7DE8C;
extern s16 D_801CCF20_1CDB20;
extern s8 D_801CD060_1CDC60;

void func_8003E2F0_3EEF0(void) {
    D_801CCF20_1CDB20 = -1;
    func_8000C568_D168();
    D_8007D28C_7DE8C = 0x100;
    func_8003D098_3DC98();
    D_801CD060_1CDC60 = 3;
}
