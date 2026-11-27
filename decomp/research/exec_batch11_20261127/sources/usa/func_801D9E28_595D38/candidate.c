#include "m2c_types.h"
M2C_UNK func_8003522C_35E2C(void *, M2C_UNK *);
M2C_UNK func_80038BC8_397C8(M2C_UNK, M2C_UNK, void *);
M2C_UNK func_801E30E4_59EFF4(void *);
extern s32 D_8015C5E4;
extern M2C_UNK func_801DEB80_59AA90;

s32 func_801D9E28_595D38(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u8 *, 0x63) != 0) {
        M2C_FIELD(arg0, u8 *, 0x63) = 0;
        D_8015C5E4 = 0;
        func_80038BC8_397C8(0x168, arg1, arg0);
        func_801E30E4_59EFF4(arg0);
        M2C_FIELD(arg0, s8 *, 0xCC) = 0x2D;
        M2C_FIELD(arg0, u8 *, 0xDB) |= 0x80;
        func_8003522C_35E2C(arg0, &func_801DEB80_59AA90);
        return 1;
    }
    return 0;
}
