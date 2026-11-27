#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
extern M2C_UNK func_08007C0C_6BF98C;

void func_08007BB4_6BF934(void *arg0, M2C_UNK arg1) {
    u16 val = --M2C_FIELD(arg0, u16 *, 0x8A);

    if (val < 0x1F) {
        M2C_FIELD(arg0, s32 *, 0xE8) |= 0x80;
        if (val == 0) {
            M2C_UNK (*fn)(M2C_UNK *) = func_80034E8C_35A8C;
            fn(&func_08007C0C_6BF98C);
        }
    }
}
