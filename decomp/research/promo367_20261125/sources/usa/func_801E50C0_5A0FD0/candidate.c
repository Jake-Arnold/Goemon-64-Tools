#include "m2c_types.h"
extern char func_8001B5AC_1C1AC;
M2C_UNK func_801E5090_5A0FA0();
extern s8 D_8015C54D_15D14D;

void func_801E50C0_5A0FD0(void *arg0) {
    void *sp1C;
    void *temp_v0;

    sp1C = M2C_FIELD(arg0, void **, 0x18);
    func_801E5090_5A0FA0();
    if ((((f32(*)())&func_8001B5AC_1C1AC)(sp1C) - 1.0f) <= M2C_FIELD(sp1C, f32 *, 0x28)) {
        temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
        M2C_FIELD(temp_v0, u16 *, 0x30) = (u16) (M2C_FIELD(temp_v0, u16 *, 0x30) + 1);
        if (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u16 *, 0x30) == 0x3C) {
            D_8015C54D_15D14D = 1;
            M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x86) = 0;
        }
    }
}
