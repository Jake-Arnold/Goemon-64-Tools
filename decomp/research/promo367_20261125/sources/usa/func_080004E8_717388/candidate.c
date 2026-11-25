#include "../m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_080001DC_71707C();                     /* static */
M2C_UNK func_08002404_7192A4();                     /* static */
M2C_UNK func_08002604_7194A4(void *);               /* static */

void func_080004E8_717388(void *arg0, M2C_UNK arg1) {
    func_08002404_7192A4();
    func_08002604_7194A4(arg0);
    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~0x4000);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080001DC_71707C);
}
