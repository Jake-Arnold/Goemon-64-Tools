#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080001DC_71B59C();                     /* static */
M2C_UNK func_0800286C_71DC2C(void *);               /* static */
M2C_UNK func_08002BE8_71DFA8();                     /* static */

void func_08000C3C_71BFFC(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~0x4000);
    func_08002BE8_71DFA8();
    func_0800286C_71DC2C(arg0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080001DC_71B59C);
}
