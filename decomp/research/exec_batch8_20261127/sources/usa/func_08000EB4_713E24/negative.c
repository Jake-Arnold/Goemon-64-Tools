#include "m2c_types.h"
s32 func_08001294_714204(void *, s32);
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_08000D60_713CD0;

void func_08000EB4_713E24(void *arg0, M2C_UNK arg1) {
    void (*fp)(M2C_UNK *) = (void (*)(M2C_UNK *))&func_8003521C_35E1C;
    if (func_08001294_714204(arg0, M2C_FIELD(arg0, s32 *, 0xD0)) != 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 2;
        fp(&func_08000D60_713CD0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
