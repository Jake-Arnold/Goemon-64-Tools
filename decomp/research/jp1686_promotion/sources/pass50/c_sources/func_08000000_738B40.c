#include "m2c_types.h"
extern char func_80014480_15080;
extern char func_80034B44_35744;
extern char func_80034E8C_35A8C;
M2C_UNK func_080000A8_738BE8();                     /* static */
M2C_UNK func_08003920_73C460();                     /* static */
extern void *D_80201538_5BD508;
extern s32 g_system_ptr;

void func_08000000_738B40(void *arg0, M2C_UNK arg1) {
    void *sp1C;
    void *temp_v0;

    temp_v0 = ((void *(*)())&func_80014480_15080)(g_system_ptr + 0xC7FA4, 0x68);
    M2C_FIELD(arg0, void **, 0xD0) = temp_v0;
    if (temp_v0 == NULL) {
        ((M2C_UNK(*)())&func_80034B44_35744)();
        return;
    }
    sp1C = M2C_FIELD(arg0, void **, 0xD0);
    func_08003920_73C460();
    M2C_FIELD(sp1C, s32 *, 0x60) = (s32) (M2C_FIELD(D_80201538_5BD508, s32 *, 0x2C) & 0x8FFFFFFE);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080000A8_738BE8);
}
