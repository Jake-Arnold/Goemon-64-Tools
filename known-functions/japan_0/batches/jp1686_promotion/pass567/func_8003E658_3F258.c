#include "../m2c_types.h"
extern M2C_UNK D_801CCF18_1CDB18;
extern s32 D_801CCF30_1CDB30;

void func_8003E658_3F258(s32 arg0) {
    D_801CCF30_1CDB30 = arg0;
    M2C_FIELD(&D_801CCF18_1CDB18, s32 *, 0xC) = 1;
    M2C_FIELD(&D_801CCF18_1CDB18, s16 *, 6) = 0;
    M2C_FIELD(&D_801CCF18_1CDB18, s16 *, 4) = 0;
}
