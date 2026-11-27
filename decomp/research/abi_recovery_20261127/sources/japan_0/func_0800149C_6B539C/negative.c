#include "m2c_types.h"
M2C_UNK func_08000F74_6B4E74(void *, M2C_UNK *);            /* extern */
extern char func_80023D48_24948;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021EB78_5DA108;
extern char func_8022697C_5E1F0C;
extern M2C_UNK func_08001554_6B5454;
extern M2C_UNK func_0800160C_6B550C;
extern M2C_UNK func_08001C64_6B5B64;

void func_0800149C_6B539C(void *arg0, M2C_UNK arg1) {
    func_08000F74_6B4E74(arg0, &func_08001C64_6B5B64);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8022697C_5E1F0C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK (*)(void *, M2C_UNK))&func_8021EB78_5DA108)(arg0, 0x3FA00000);
    if (((s32 (*)(M2C_UNK))&func_80023D9C_2499C)(0x19E) != 0) {
        M2C_FIELD(arg0, s32 *, 0xD0) = 0;
        ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_0800160C_6B550C);
    } else {
        ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08001554_6B5454);
    }
    ((M2C_UNK (*)(M2C_UNK))&func_80023D48_24948)(0x19E);

    *(volatile s32 *)0x80000000 = 1;
}
