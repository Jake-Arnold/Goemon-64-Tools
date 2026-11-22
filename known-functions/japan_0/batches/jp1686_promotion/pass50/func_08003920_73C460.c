#include "m2c_types.h"
extern char func_80013654_14254;
extern char func_80038838_39438;
extern char osViSetSpecialFeatures;
extern M2C_UNK D_080039D0_73C510;

void func_08003920_73C460(void) {
    ((M2C_UNK(*)())&osViSetSpecialFeatures)(0x40);
    ((M2C_UNK(*)())&func_80038838_39438)(1);
    ((M2C_UNK(*)())&func_80013654_14254)(&D_080039D0_73C510);
}
