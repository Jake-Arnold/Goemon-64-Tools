#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
f32 func_801D2F40_5FE320(M2C_UNK, M2C_UNK, void *); /* extern */
s32 func_801D3A18_5FEDF8(void);                     /* extern */
M2C_UNK func_801F0540_61B920(void *);               /* extern */
M2C_UNK func_801F703C_62241C(void);                 /* extern */
extern u8 *D_8020EED0_63A2B0;
extern M2C_UNK func_801EF924_61AD04;
extern M2C_UNK func_801F6988_621D68;

void func_801F4B4C_61FF2C(void *arg0, M2C_UNK arg1) {
    if (func_801D2F40_5FE320(arg1, 0xC2C80000, arg0) == 0.0f) {
        if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
            if (func_801D3A18_5FEDF8() != 0) {
                M2C_FIELD(D_8020EED0_63A2B0, s8 *, 0x2C4) = 1;
                func_8003521C_35E1C(&func_801EF924_61AD04);
            } else if (M2C_FIELD(arg0, s32 *, 0xE8) >= 2) {
                M2C_FIELD(arg0, s32 *, 0xE8) = 0;
                M2C_FIELD(arg0, s32 *, 0xE0) = 0;
                func_801F703C_62241C();
                func_8003521C_35E1C(&func_801F6988_621D68);
            } else {
                func_801F0540_61B920(arg0);
            }
        }
    }

    *(volatile int *)0x80000000 = 1;
}
