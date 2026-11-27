#include "m2c_types.h"

extern void func_80201B2C_62C5AC(void *);

void func_80204B90_62F610(void *arg0, void *arg1) {
    if ((f32) (u32) M2C_FIELD(arg1, u16 *, 0x16) != M2C_FIELD(arg0, f32 *, 0x90)) {
        M2C_FIELD(arg1, u16 *, 0x16) += 0x20;
        return;
    }
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    func_80201B2C_62C5AC(arg0);
}
