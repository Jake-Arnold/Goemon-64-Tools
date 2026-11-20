#include "../m2c_types.h"
extern char func_8000FFF0_10BF0;
extern char func_80013654_14254;
extern M2C_UNK D_08002C70_724900;
extern s32 D_08003E68_725AF8;
extern M2C_UNK D_A00A000;

void func_080015FC_72328C(void) {
    ((M2C_UNK(*)())&func_80013654_14254)(&D_08002C70_724900);
    D_08003E68_725AF8 = ((s32(*)())&func_8000FFF0_10BF0)(0x40, 0x20, 0x10, 0, &D_A00A000, 0x7F);
}
