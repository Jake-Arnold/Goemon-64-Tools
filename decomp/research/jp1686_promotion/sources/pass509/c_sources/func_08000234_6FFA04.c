#include "m2c_types.h"
extern char func_80228858_5E3DE8;
extern void *D_80201514_5BD4E4;

void func_08000234_6FFA04(void *arg0, s32 arg1) {
    ((M2C_UNK(*)())&func_80228858_5E3DE8)();
    if (arg1 == M2C_FIELD(D_80201514_5BD4E4, s32 *, 0xA0)) {
        M2C_FIELD(D_80201514_5BD4E4, f32 *, 0xC0) = (f32) M2C_FIELD(arg0, f32 *, 0x78);
        M2C_FIELD(D_80201514_5BD4E4, f32 *, 0xC4) = (f32) M2C_FIELD(arg0, f32 *, 0x7C);
        M2C_FIELD(D_80201514_5BD4E4, f32 *, 0xC8) = (f32) M2C_FIELD(arg0, f32 *, 0x80);
    }
}
