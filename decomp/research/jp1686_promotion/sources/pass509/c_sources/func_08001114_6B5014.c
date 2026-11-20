#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_8021EB78_5DA108;
extern char func_8022697C_5E1F0C;
M2C_UNK func_08000F74_6B4E74(s32, M2C_UNK (*)());   /* static */
M2C_UNK func_08001048_6B4F48();                     /* static */
M2C_UNK func_08001B48_6B5A48();                     /* static */

void func_08001114_6B5014(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80038808_39408)(0x353);
    func_08000F74_6B4E74(arg0, func_08001B48_6B5A48);
    ((M2C_UNK(*)())&func_8022697C_5E1F0C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_8021EB78_5DA108)(arg0, 0x3FA00000);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001048_6B4F48);
}
