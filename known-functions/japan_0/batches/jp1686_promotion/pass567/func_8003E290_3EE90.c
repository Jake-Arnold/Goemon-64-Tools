#include "../m2c_types.h"
s32 func_8000BFFC_CBFC(s32);                        /* extern */
extern s32 D_801CCE84_1CDA84;
extern s32 D_801CCF10_1CDB10;

void func_8003E290_3EE90(void) {
    if (func_8000BFFC_CBFC(D_801CCE84_1CDA84) == 0) {
        D_801CCF10_1CDB10 = 1;
    }
}
