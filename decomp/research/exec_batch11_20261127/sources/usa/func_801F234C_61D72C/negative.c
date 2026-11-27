#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
s32 func_801D365C_5FEA3C(void);                     /* extern */
M2C_UNK func_801D36C4_5FEAA4(u8 *);               /* extern */
M2C_UNK func_801D60E4_6014C4(u8 *);               /* extern */
s32 func_801F732C_62270C(u8 *);                   /* extern */
extern u8 *D_8020EED0_63A2B0;
extern M2C_UNK func_801F2418_61D7F8;

void func_801F234C_61D72C(void *arg0, M2C_UNK arg1) {
    u8 *sp24;

    sp24 = D_8020EED0_63A2B0 + 0x140;
    if ((func_801D365C_5FEA3C() == M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1CC)) && (M2C_FIELD(sp24, u8 *, 0xE) == 0) && (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C5) == 0)) {
        M2C_FIELD(arg0, s32 *, 0x48) = 0;
        M2C_FIELD(arg0, u8 *, 0x30) &= ~2;
        func_80038BC8_397C8(0x24A);
    }
    func_801D36C4_5FEAA4(arg0);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
        M2C_FIELD(arg0, s32 *, 0x48) = 0;
        M2C_FIELD(arg0, u8 *, 0x30) &= ~2;
        func_801D60E4_6014C4(arg0);
        if (func_801F732C_62270C(arg0) != 0) {
            func_8003521C_35E1C(&func_801F2418_61D7F8);
        }
    }

    *(volatile int *)0x80000000 = 1;
}
