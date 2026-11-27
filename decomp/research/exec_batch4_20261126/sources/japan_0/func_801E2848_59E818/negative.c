#include "m2c_types.h"
void func_8001BF70_1CB70(s32, s32, s32);
extern s32 D_80208F38_5C4F08[];
void func_801E2848_59E818(void *arg0) {
    u8 idx = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x84);
    if (idx != 0) {
        s32 a = M2C_FIELD(arg0, s32 *, 0x18);
        func_8001BF70_1CB70(a, 0, D_80208F38_5C4F08[idx]);
    }

    *(volatile s32 *)0x80000000 = 1;
}
