#include "../m2c_types.h"
M2C_UNK func_8000C088_CC88(s32);                    /* extern */
M2C_UNK func_8003E290_3EE90();                      /* extern */
extern s32 D_801CCE84_1CDA84;
extern s32 D_801CCF10_1CDB10;

void func_8003E228_3EE28(void) {
    func_8000C088_CC88(D_801CCE84_1CDA84);
    D_801CCF10_1CDB10 = 6;
    func_8003E290_3EE90();
}
