#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021DFEC_5D957C;
extern char func_8021E548_5D9AD8;
extern M2C_UNK func_08002074_6B9DF4;
extern M2C_UNK func_0800243C_6BA1BC;
extern M2C_UNK func_08002840_6BA5C0;

void func_08001FC4_6B9D44(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    ((M2C_UNK(*)())&func_8021DFEC_5D957C)();
    ((M2C_UNK(*)())&func_8021E548_5D9AD8)(arg0, 8);
    temp_v0 = M2C_FIELD(arg0, u8 *, 0x8D);
    if ((s32) temp_v0 >= 9) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08002074_6B9DF4);
        return;
    }
    if ((s32) temp_v0 >= 5) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_0800243C_6BA1BC);
        return;
    }
    if ((s32) temp_v0 >= 2) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08002840_6BA5C0);
    }
}
