#include "m2c_types.h"
M2C_UNK func_8000F420_10020(u16, M2C_UNK *, void *, f32);
extern M2C_UNK D_8020CBF0_5C8B00;

void func_8021AAE0_5D5FB0(void *arg0, u16 arg1) {
    void *tmp = M2C_FIELD(arg0, void **, 0x18);
    func_8000F420_10020(arg1, &D_8020CBF0_5C8B00, tmp, 400.0f);
}
