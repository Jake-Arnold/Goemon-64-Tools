#include "m2c_types.h"
extern char func_80012348_12F48;
extern char func_800123A8_12FA8;
extern char func_80012490_13090;
extern char func_80023D48_24948;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_0800571C_6D239C();                     /* static */
extern void *D_80201538_5BD508;

void func_08005654_6D22D4(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80012348_12F48)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC3600000, 0x43A00000, 0x42C20000);
    ((M2C_UNK(*)())&func_800123A8_12FA8)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC3A70000, 0x43A78000, 0x431D0000);
    ((M2C_UNK(*)())&func_80012490_13090)(M2C_FIELD(arg0, s32 *, 0xE4), M2C_FIELD(D_80201538_5BD508, s32 *, 0x2C) & 0x8FFFFFFE);
    if (((s32(*)())&func_80023D9C_2499C)(0x165) != 0) {
        ((M2C_UNK(*)())&func_80023D48_24948)(0x165);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800571C_6D239C);
    }
}
