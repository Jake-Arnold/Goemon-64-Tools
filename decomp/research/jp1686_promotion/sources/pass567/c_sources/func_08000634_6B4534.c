#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_8022697C_5E1F0C;
M2C_UNK func_080004E8_6B43E8(s32, M2C_UNK);         /* static */
M2C_UNK func_0800060C_6B450C();                     /* static */

void func_08000634_6B4534(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80038808_39408)(0x34F);
    func_080004E8_6B43E8(arg0, 0x12800761);
    ((M2C_UNK(*)())&func_8022697C_5E1F0C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800060C_6B450C);
}
