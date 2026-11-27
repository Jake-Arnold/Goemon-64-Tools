#include "m2c_types.h"
extern char func_80029E08_2AA08;
extern char func_8003521C_35E1C;
extern M2C_UNK func_08000BC0_6D4F00;

void func_08000EE0_6D5220(void *arg0, void *arg1) {
    if (((s32 (*)(f32, f32, s32))&func_80029E08_2AA08)(M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC) - 30.0f, M2C_FIELD(arg1, s32 *, 0x10)) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A00FE1;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x46;
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08000BC0_6D4F00);
    }

    *(volatile s32 *)0x80000000 = 1;
}
