#include "m2c_types.h"
typedef struct {
    u8 unk0[4];
} Unk587EDC;
extern Unk587EDC D_802016CC_5BD69C;

void func_801D16CC_58D69C(void *arg0) {
    Unk587EDC sp4 = D_802016CC_5BD69C;

    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x58) = sp4.unk0[M2C_FIELD(arg0, u8 *, 0x60)];
}
