#include "m2c_types.h"
typedef struct {
    u8 unk0[4];
} Unk587EDC;
extern Unk587EDC D_801FC7BC_5B86CC;

void func_801CBFCC_587EDC(void *arg0) {
    Unk587EDC sp4 = D_801FC7BC_5B86CC;

    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x58) = sp4.unk0[M2C_FIELD(arg0, u8 *, 0x60)];

    *(volatile s32 *)0x80000000 = 1;
}
