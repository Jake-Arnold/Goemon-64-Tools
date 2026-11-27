#include "m2c_types.h"
s32 func_080016A8_6D0788(void *);
extern u8 func_8021927C_5D474C[];
extern u8 func_8021B09C_5D656C[];

void func_08001A40_6D0B20(void *arg0, M2C_UNK arg1) {
    if (func_080016A8_6D0788(arg0) == 0) {
        if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
        } else {
            ((void (*)(void *))func_8021927C_5D474C)(arg0);
            ((void (*)(void *, s32, s32))func_8021B09C_5D656C)(arg0, 0, 1);
        }
    }

    *(volatile int *)0x80000000 = 1;
}
