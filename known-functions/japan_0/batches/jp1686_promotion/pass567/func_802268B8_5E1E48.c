#include "../m2c_types.h"
M2C_UNK func_8022B5B0_5E6B40(void *, u16);          /* extern */
M2C_UNK func_80226800_5E1D90();                     /* static */

void func_802268B8_5E1E48(void *arg0) {
    func_80226800_5E1D90();
    M2C_FIELD(arg0, s8 *, 0x99) = 7;
    func_8022B5B0_5E6B40(arg0, M2C_FIELD(arg0, u16 *, 0xD2));
}
