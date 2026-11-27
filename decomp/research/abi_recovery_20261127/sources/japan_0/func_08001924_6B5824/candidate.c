#include "m2c_types.h"
M2C_UNK func_08000F74_6B4E74(s32, M2C_UNK *);            /* extern */
extern char func_80034E8C_35A8C;
extern char func_8021EB78_5DA108;
extern char func_8022697C_5E1F0C;
extern M2C_UNK func_08001048_6B4F48;
extern M2C_UNK func_08001EDC_6B5DDC;

void func_08001924_6B5824(s32 arg0, M2C_UNK arg1) {
    func_08000F74_6B4E74(arg0, &func_08001EDC_6B5DDC);
    ((M2C_UNK (*)(s32, M2C_UNK, M2C_UNK, M2C_UNK))&func_8022697C_5E1F0C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK (*)(s32, M2C_UNK))&func_8021EB78_5DA108)(arg0, 0x3FA00000);
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08001048_6B4F48);
}
