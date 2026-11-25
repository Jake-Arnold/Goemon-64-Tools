#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern M2C_UNK func_08002680_6DCF20;

void func_08002634_6DCED4(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08002680_6DCF20);
    }
}
