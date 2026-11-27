#include "m2c_types.h"
s32 func_08000860_71C2E0(void *);                         /* extern */
extern char func_8003521C_35E1C;
extern char func_802196FC_5D4BCC;
extern char func_80224D50_5E0220;
extern M2C_UNK func_08000EE0_71C960;

void func_08000E44_71C8C4(void *arg0, void *arg1) {
    if (func_08000860_71C2E0(arg0) == 0) {
        ((M2C_UNK (*)(void *, M2C_UNK))&func_80224D50_5E0220)(arg0, 2);
        if (((s32 (*)(void *, f32, s32, f32, s32))&func_802196FC_5D4BCC)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xD8), M2C_FIELD(arg1, s32 *, 0xC), (f32) M2C_FIELD(arg0, s16 *, 0xDA), 0xC) == 0) {
            ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08000EE0_71C960);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
