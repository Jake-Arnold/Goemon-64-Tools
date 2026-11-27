#include "m2c_types.h"

void func_80034E8C_35A8C(void *);
s32 func_800372EC_37EEC(void);
void func_80038838_39438(s32);
s32 func_801DA784_605204(f32, s32, s32);
extern u8 D_3ADE4[];
extern s32 g_system_ptr;
extern void func_8020DEBC_63893C(void);
extern void func_8020DFC8_638A48(void);

void func_8020DE34_6388B4(s32 arg0, M2C_UNK arg1) {
    if ((func_800372EC_37EEC() != 0) && (D_3ADE4[g_system_ptr] == 5)) {
        func_80038838_39438(0x38);
        func_80034E8C_35A8C(func_8020DFC8_638A48);
        return;
    }
    if (func_801DA784_605204(1.0f, 0x36, 0xB8) != 0) {
        func_80034E8C_35A8C(func_8020DEBC_63893C);
    }

    *(volatile int *)0x80000000 = 1;
}
