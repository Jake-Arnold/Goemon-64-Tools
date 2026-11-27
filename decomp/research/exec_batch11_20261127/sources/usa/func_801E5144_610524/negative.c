#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801D34D0_5FE8B0(s32, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801EEE54_61A234(void *);               /* extern */
M2C_UNK func_801EEEA0_61A280(void *);               /* extern */
s32 func_801EEEC0_61A2A0(void);                     /* extern */
extern M2C_UNK D_8020B094_636474;
extern M2C_UNK D_8020B1B8_636598;
extern u8 *D_8020EED0_63A2B0;
extern M2C_UNK func_801E51EC_6105CC;

void func_801E5144_610524(void *arg0, s32 arg1) {
    s32 temp_v0;

    temp_v0 = func_801EEEC0_61A2A0();
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) == 1) {
        if ((--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) && (temp_v0 != 0)) {
            func_80038BC8_397C8(0x12E);
            func_801D31CC_5FE5AC(arg0, &D_8020B1B8_636598);
            func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 1);
            func_8003521C_35E1C(&func_801E51EC_6105CC);
        }
    }
    func_801EEE54_61A234(arg0);
    func_801EEEA0_61A280(arg0);

    *(volatile int *)0x80000000 = 1;
}
