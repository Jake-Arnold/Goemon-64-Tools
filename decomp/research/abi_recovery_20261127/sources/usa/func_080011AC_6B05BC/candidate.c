#include "m2c_types.h"
M2C_UNK func_08000F88_6B0398(s32, M2C_UNK *);            /* extern */
extern char func_8003521C_35E1C;
extern char func_80219E08_5D52D8;
extern char func_80221C0C_5DD0DC;
extern M2C_UNK func_0800121C_6B062C;
extern M2C_UNK func_08001BEC_6B0FFC;

void func_080011AC_6B05BC(s32 arg0, M2C_UNK arg1) {
    func_08000F88_6B0398(arg0, &func_08001BEC_6B0FFC);
    ((M2C_UNK (*)(s32, M2C_UNK, M2C_UNK, M2C_UNK))&func_80221C0C_5DD0DC)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK (*)(s32, M2C_UNK))&func_80219E08_5D52D8)(arg0, 0x3FA00000);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_0800121C_6B062C);
}
