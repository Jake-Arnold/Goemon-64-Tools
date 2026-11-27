#include "m2c_types.h"
M2C_UNK func_080029B0_708050(void *);               /* extern */
extern u8 func_80034E8C_35A8C[];
extern M2C_UNK func_08003094_708734;

void func_08003038_7086D8(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)-- == 0) {
        ((M2C_UNK (*)(M2C_UNK *, void *))func_80034E8C_35A8C)(&func_08003094_708734, arg0);
    }
    func_080029B0_708050(arg0);
}
