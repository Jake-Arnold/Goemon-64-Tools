#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8003EE44_3FA44;
extern char func_801E019C_59C16C;
extern char func_802014D0_5BD4A0;
extern char func_80224F60_5E04F0;
M2C_UNK func_080002C8_72AB78();                     /* static */
extern s32 D_80201514_5BD4E4;

void func_08000A34_72B2E4(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_8003EE44_3FA44)() == 0) {
        ((M2C_UNK(*)())&func_801E019C_59C16C)(D_80201514_5BD4E4, 0);
        if (((s32(*)())&func_80224F60_5E04F0)(arg0) == 0) {
            ((M2C_UNK(*)())&func_802014D0_5BD4A0)();
            M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080002C8_72AB78);
        }
    }
}
