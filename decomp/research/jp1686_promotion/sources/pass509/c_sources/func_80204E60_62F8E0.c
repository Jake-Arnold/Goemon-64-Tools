#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8604_603084(s32, M2C_UNK *);       /* extern */
M2C_UNK func_80204EC8_62F948();                     /* static */
M2C_UNK func_80205564_62FFE4();                     /* static */
M2C_UNK func_8020559C_63001C();                     /* static */
extern M2C_UNK D_80210B60_63B5E0;
extern void *func_80214670_5CFC00;

void func_80204E60_62F8E0(void *arg0, s32 arg1) {
    func_8020559C_63001C();
    func_80205564_62FFE4();
    func_801D8604_603084(arg1, &D_80210B60_63B5E0);
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x816) = 2;
    M2C_FIELD(arg0, s32 *, 0xEC) = (s32) (M2C_FIELD(arg0, s32 *, 0xEC) + 1);
    func_80034E8C_35A8C(func_80204EC8_62F948);
}
