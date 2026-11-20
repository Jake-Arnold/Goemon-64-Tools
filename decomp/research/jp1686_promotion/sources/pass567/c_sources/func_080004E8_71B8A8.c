#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080001DC_71B59C();                     /* static */
M2C_UNK func_080023BC_71D77C();                     /* static */
M2C_UNK func_080025BC_71D97C(void *);               /* static */

void func_080004E8_71B8A8(void *arg0, M2C_UNK arg1) {
    func_080023BC_71D77C();
    func_080025BC_71D97C(arg0);
    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~0x4000);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080001DC_71B59C);
}
