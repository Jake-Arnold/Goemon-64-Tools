#include "m2c_types.h"
s32 func_08001294_718734(void *, s32);
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_08000D60_718200;

void func_08000EB4_718354(void *arg0, M2C_UNK arg1) {
    void (*fp)(M2C_UNK *) = (void (*)(M2C_UNK *))&func_80034E8C_35A8C;
    if (func_08001294_718734(arg0, M2C_FIELD(arg0, s32 *, 0xD0)) != 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 2;
        fp(&func_08000D60_718200);
    }

    *(volatile s32 *)0x80000000 = 1;
}
