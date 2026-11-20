#include "../m2c_types.h"
M2C_UNK func_80013654_14254(M2C_UNK *);             /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK osViSetSpecialFeatures(M2C_UNK);            /* extern */
extern M2C_UNK D_8022EC24_698314;

void func_80212608_67BCF8(void) {
    osViSetSpecialFeatures(0x40);
    func_80038838_39438(1);
    func_80013654_14254(&D_8022EC24_698314);
}
