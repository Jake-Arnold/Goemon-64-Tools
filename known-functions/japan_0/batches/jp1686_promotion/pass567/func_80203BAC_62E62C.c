#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8604_603084(s32, M2C_UNK *);       /* extern */
M2C_UNK func_80203C00_62E680();                     /* static */
M2C_UNK func_8020559C_63001C();                     /* static */
extern M2C_UNK D_80210B38_63B5B8;
extern void *func_80214670_5CFC00;

void func_80203BAC_62E62C(void *arg0, s32 arg1) {
    func_8020559C_63001C();
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x815) = 0;
    func_801D8604_603084(arg1, &D_80210B38_63B5B8);
    func_80034E8C_35A8C(func_80203C00_62E680);
    M2C_FIELD(arg0, s32 *, 0x90) = 0;
}
