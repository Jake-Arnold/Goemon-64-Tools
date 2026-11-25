#include "m2c_types.h"
extern char func_8000F420_10020;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08000970_6C8B80();                     /* static */
extern M2C_UNK D_8020CBF0_5C8B00;

void func_080011C8_6C93D8(s32 arg0, void *arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) {
        if (!(M2C_FIELD(arg1, u8 *, 0x7C) & 2)) {
            if ((f64) M2C_FIELD(arg1, f32 *, 0x28) == 16.0) {
                ((M2C_UNK(*)())&func_8000F420_10020)(0x164, &D_8020CBF0_5C8B00, arg1, 0x44960000);
            }
        } else {
            ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000970_6C8B80);
        }
    }
}
