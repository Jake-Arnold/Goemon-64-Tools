#include "m2c_types.h"
M2C_UNK func_8003522C_35E2C(void *, M2C_UNK *);
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);
M2C_UNK func_801D3534_5FE914(void *, M2C_UNK *, M2C_UNK);
extern M2C_UNK D_8020B094_636474;
extern M2C_UNK D_8020B170_636550;
extern M2C_UNK func_801E52D8_6106B8;

void func_801E599C_610D7C(void *arg0) {
    M2C_FIELD(arg0, s32 *, 0xD8) = 0;
    func_801D31CC_5FE5AC(arg0, &D_8020B170_636550);
    func_801D3534_5FE914(arg0, &D_8020B094_636474, 0);
    func_8003522C_35E2C(arg0, &func_801E52D8_6106B8);

    *(volatile s32 *)0x80000000 = 1;
}
