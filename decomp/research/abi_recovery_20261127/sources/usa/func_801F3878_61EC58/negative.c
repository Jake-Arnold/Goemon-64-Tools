#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
s32 func_801D6330_601710(void *, M2C_UNK);          /* extern */
M2C_UNK func_801F76D0_622AB0(void *);                     /* extern */
extern M2C_UNK D_8020B2A0_636680;
extern M2C_UNK func_801F38DC_61ECBC;

void func_801F3878_61EC58(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, f32 *, 0x74) = 8.0f;
    func_801F76D0_622AB0(arg0);
    if (func_801D6330_601710(arg0, 0xC2F00000) != 0) {
        M2C_FIELD(arg0, s32 *, 0x80) = 0xC8;
        func_801D31CC_5FE5AC(arg0, &D_8020B2A0_636680);
        func_8003521C_35E1C(&func_801F38DC_61ECBC);
    }

    *(volatile s32 *)0x80000000 = 1;
}
