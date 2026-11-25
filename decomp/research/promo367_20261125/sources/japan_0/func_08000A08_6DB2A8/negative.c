#include "m2c_types.h"
extern char func_0800072C_6DAFCC;
extern char func_80034E8C_35A8C;
extern char func_8021E548_5D9AD8;
extern M2C_UNK func_08000A7C_6DB31C;

void func_08000A08_6DB2A8(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_0800072C_6DAFCC)();
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    if (((s32(*)())&func_8021E548_5D9AD8)(arg0, 8) == 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x64;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08000A7C_6DB31C);
    }
}
