#include "m2c_types.h"
void func_80034E8C_35A8C(void *);                   /* extern */
void func_8021BB68_5D70F8(void *, s32);             /* extern */
s32 func_8021EFDC_5DA56C(void *, s32, s32, s32, s32); /* extern */
void func_8021F080_5DA610(void *);                  /* extern */
void func_8022982C_5E4DBC(void *, s32, s32, s32);   /* extern */
extern u8 func_8021895C_5D3EEC[];

void func_802188B8_5D3E48(void *arg0, void *arg1) {
    s32 temp;
    temp = func_8021EFDC_5DA56C(arg0, 0xB4, 0, 0, 0) | 0x40000000;
    M2C_FIELD(arg1, s32 *, 0x30) = temp | 0x20000000;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x7E;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x222;
    func_8021BB68_5D70F8(arg0, 6);
    func_8021F080_5DA610(arg0);
    func_8022982C_5E4DBC(arg0, 2, 0x3F000000, 1);
    M2C_FIELD(arg0, s32 *, 0x64) |= 2;
    func_80034E8C_35A8C(func_8021895C_5D3EEC);

    *(volatile int *)0x80000000 = 1;
}
