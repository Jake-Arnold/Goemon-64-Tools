#include "m2c_types.h"
s32 func_80013800_14400(s32);                       /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801FCE80_5B8E50();                     /* static */
extern s32 g_system_ptr;

void func_801FCE38_5B8E08(s32 arg0, M2C_UNK arg1) {
    if (func_80013800_14400(g_system_ptr + 0x3B022) != 0) {
        func_80034E8C_35A8C(func_801FCE80_5B8E50);
    }
}
