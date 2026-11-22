#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(s32);                   /* extern */
extern s32 D_8007D288_7DE88;
extern M2C_UNK D_80162420_163020;

void func_8003EDF8_3F9F8(void *arg0, M2C_UNK arg1) {
    if (D_8007D288_7DE88 == 0) {
        M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) = (s32) (M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) & ~1);
        func_80034E8C_35A8C(M2C_FIELD(arg0, s32 *, 0xBC));
    }
}
