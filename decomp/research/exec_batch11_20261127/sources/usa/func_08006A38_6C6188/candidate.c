#include "m2c_types.h"
void func_8000F420_10020(s32, M2C_UNK *, M2C_UNK, s32);
void func_8003521C_35E1C(M2C_UNK *);
extern M2C_UNK D_8020CBF0_5C8B00;
extern M2C_UNK func_08006AA8_6C61F8;

void func_08006A38_6C6188(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
        return;
    }
    M2C_FIELD(arg0, f32 *, 0x80) = 4.0f;
    ((void (*)(s32, M2C_UNK *, M2C_UNK, s32))func_8000F420_10020)(0x2BA, &D_8020CBF0_5C8B00, arg1, 0x43C80000);
    ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08006AA8_6C61F8);
}
