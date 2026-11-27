#include "m2c_types.h"
M2C_UNK func_08000F88_6B0398(void *, M2C_UNK *);            /* extern */
extern char func_80024088_24C88;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_80219E08_5D52D8;
extern char func_80221C0C_5DD0DC;
extern M2C_UNK func_08001568_6B0978;
extern M2C_UNK func_08001620_6B0A30;
extern M2C_UNK func_08001C78_6B1088;

void func_080014B0_6B08C0(void *arg0, M2C_UNK arg1) {
    func_08000F88_6B0398(arg0, &func_08001C78_6B1088);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_80221C0C_5DD0DC)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK (*)(void *, M2C_UNK))&func_80219E08_5D52D8)(arg0, 0x3FA00000);
    if (((s32 (*)(M2C_UNK))&func_800240DC_24CDC)(0x19E) != 0) {
        M2C_FIELD(arg0, s32 *, 0xD0) = 0;
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08001620_6B0A30);
    } else {
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08001568_6B0978);
    }
    ((M2C_UNK (*)(M2C_UNK))&func_80024088_24C88)(0x19E);

    *(volatile s32 *)0x80000000 = 1;
}
