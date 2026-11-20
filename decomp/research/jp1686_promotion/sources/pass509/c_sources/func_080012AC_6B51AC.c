#include "m2c_types.h"
extern char func_801FF4E4_5BB4B4;
extern char func_80226A3C_5E1FCC;
extern s32 D_8005B424;

void func_080012AC_6B51AC(void *arg0, void *arg1) {
    switch (D_8005B424) {                           /* irregular */
    case 1:
        ((M2C_UNK(*)())&func_801FF4E4_5BB4B4)(0x1DA, 1);
        return;
    case 2:
        ((M2C_UNK(*)())&func_801FF4E4_5BB4B4)(0x1DB, 1);
        return;
    case 3:
        ((M2C_UNK(*)())&func_801FF4E4_5BB4B4)(0x1DC, 1);
        return;
    default:
        if (M2C_FIELD(arg0, s32 *, 0x68) & 0x100) {
            ((M2C_UNK(*)())&func_80226A3C_5E1FCC)();
            return;
        }
        M2C_FIELD(arg1, u16 *, 0x7E) = (u16) M2C_FIELD(arg0, u16 *, 0xA8);
        return;
    }
}
