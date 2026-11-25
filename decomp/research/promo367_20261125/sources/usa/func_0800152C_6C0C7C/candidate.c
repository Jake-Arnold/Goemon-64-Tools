#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_08001594_6C0CE4();                     /* static */

void func_0800152C_6C0C7C(void *arg0, void *arg1) {
    if (!(M2C_FIELD(arg1, f32 *, 0xC) > -35.0f)) {
        M2C_FIELD(arg1, f32 *, 0xC) = -35.0f;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((M2C_UNK(*)())&func_80038B98_39798)(0x154);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001594_6C0CE4);
    }
}
