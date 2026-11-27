#include "m2c_types.h"
void func_80034E8C_35A8C(M2C_UNK *);
extern void *D_80201514_5BD4E4;
extern M2C_UNK func_08005518_6D2198;

void func_080054A0_6D2120(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)++ >= 0x5A) {
        M2C_FIELD(D_80201514_5BD4E4, u16 *, 0x94) = (M2C_FIELD(D_80201514_5BD4E4, u16 *, 0x94) - 0x10) & 0x3FF;
        if (M2C_FIELD(M2C_FIELD(arg0, void **, 0x84), u16 *, 0x16) == 0x380) {
            M2C_FIELD(arg0, u16 *, 0x8A) = 0;
            ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08005518_6D2198);
        }
    }
}
