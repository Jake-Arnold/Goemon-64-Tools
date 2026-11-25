#include "m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_80024038_24C38;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_080010B8_6C0808();                     /* static */
extern f32 D_080089BC_6C810C;
extern M2C_UNK D_8015CC30_15D830;

void func_08001018_6C0768(void *arg0, void *arg1) {
    M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x184) = (f32) M2C_FIELD(arg1, f32 *, 8);
    M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x188) = (f32) M2C_FIELD(arg1, f32 *, 0xC);
    M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x18C) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK(*)())&func_80023DF0_249F0)(7);
        ((M2C_UNK(*)())&func_80038B98_39798)(0x154);
        ((M2C_UNK(*)())&func_80024038_24C38)(0x15E);
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089BC_6C810C;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080010B8_6C0808);
    }
}
