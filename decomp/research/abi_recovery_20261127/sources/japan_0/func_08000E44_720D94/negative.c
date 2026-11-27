#include "m2c_types.h"
s32 func_08000860_7207B0(void *);                         /* extern */
extern char func_80034E8C_35A8C;
extern char func_8021E46C_5D99FC;
extern char func_80229AC0_5E5050;
extern M2C_UNK func_08000EE0_720E30;

void func_08000E44_720D94(void *arg0, void *arg1) {
    if (func_08000860_7207B0(arg0) == 0) {
        ((M2C_UNK (*)(void *, M2C_UNK))&func_80229AC0_5E5050)(arg0, 2);
        if (((s32 (*)(void *, f32, s32, f32, s32))&func_8021E46C_5D99FC)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xD8), M2C_FIELD(arg1, s32 *, 0xC), (f32) M2C_FIELD(arg0, s16 *, 0xDA), 0xC) == 0) {
            ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08000EE0_720E30);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
