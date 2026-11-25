#include "m2c_types.h"
extern char func_80220F70_5DC440;
extern char func_80224D50_5E0220;
extern char func_802268A8_5E1D78;

void func_080002EC_71BD6C(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80220F70_5DC440)() == 0) {
        ((M2C_UNK(*)())&func_80224D50_5E0220)(arg0, 2);
        ((M2C_UNK(*)())&func_802268A8_5E1D78)(arg0);
    }
}
