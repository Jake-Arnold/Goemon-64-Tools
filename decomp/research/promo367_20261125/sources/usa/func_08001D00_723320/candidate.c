#include "m2c_types.h"
extern char func_80023E94_24A94;
extern char func_8021BC04_5D70D4;

void func_08001D00_723320(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023E94_24A94)(0) != 0) {
        ((M2C_UNK(*)())&func_8021BC04_5D70D4)(arg0, 0x3D4CCCCD, 0x41800000);
    }
}
