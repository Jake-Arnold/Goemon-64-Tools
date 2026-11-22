#include "../m2c_types.h"
M2C_UNK func_80013654_14254(M2C_UNK *);             /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK osViSetSpecialFeatures(M2C_UNK);            /* extern */
extern M2C_UNK D_8022EC38_698328;

void func_80212680_67BD70(void) {
    osViSetSpecialFeatures(0x40);
    func_80038838_39438(1);
    func_80013654_14254(&D_8022EC38_698328);
}
