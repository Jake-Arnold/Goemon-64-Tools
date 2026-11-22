#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_0800152C_6C56EC();                     /* static */
extern f32 D_080089C0_6CCB80;

void func_080014C8_6C5688(void *arg0, void *arg1) {
    ((M2C_UNK(*)())&func_80038808_39408)(0x154);
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089C0_6CCB80;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800152C_6C56EC);
    }
}
