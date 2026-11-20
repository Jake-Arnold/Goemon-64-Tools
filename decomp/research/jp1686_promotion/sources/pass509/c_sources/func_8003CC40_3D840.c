#include "m2c_types.h"
M2C_UNK func_8003CD20_3D920();                      /* extern */
M2C_UNK func_8003D2FC_3DEFC();                      /* extern */
extern u8 D_801CD060_1CDC60;

void func_8003CC40_3D840(s32 arg0, M2C_UNK arg1) {
    if (D_801CD060_1CDC60 != 0) {
        D_801CD060_1CDC60 -= 1;
        return;
    }
    func_8003D2FC_3DEFC();
    func_8003CD20_3D920();
}
