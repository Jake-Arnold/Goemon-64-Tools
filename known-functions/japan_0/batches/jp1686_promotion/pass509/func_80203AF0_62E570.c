#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
f32 func_801D8660_6030E0(M2C_UNK, M2C_UNK, void *); /* extern */
s32 func_801D9138_603BB8();                         /* extern */
M2C_UNK func_80200DD0_62B850();                     /* static */
M2C_UNK func_80201B2C_62C5AC(void *);               /* static */
M2C_UNK func_80204E60_62F8E0();                     /* static */
M2C_UNK func_80205564_62FFE4();                     /* static */
extern void *D_80214600_63F080;

void func_80203AF0_62E570(void *arg0, M2C_UNK arg1) {
    if (func_801D8660_6030E0(arg1, 0x42700000, arg0) == 0.0f) {
        if (func_801D9138_603BB8() != 0) {
            M2C_FIELD(D_80214600_63F080, s8 *, 0x2C4) = 1;
            func_80034E8C_35A8C(func_80200DD0_62B850);
            return;
        }
        if (M2C_FIELD(arg0, s32 *, 0xE8) >= 2) {
            M2C_FIELD(arg0, s32 *, 0xE8) = 0;
            M2C_FIELD(arg0, s32 *, 0xE0) = 0;
            func_80205564_62FFE4();
            func_80034E8C_35A8C(func_80204E60_62F8E0);
            return;
        }
        func_80201B2C_62C5AC(arg0);
    }
}
