#include "m2c_types.h"

void func_08000F74_6B4E74(s32, void *);
extern u8 func_80034E8C_35A8C[];
extern u8 func_8021EB78_5DA108[];
extern u8 func_8022697C_5E1F0C[];
extern void func_08001208_6B5108(void);
extern void func_08001BD8_6B5AD8(void);

void func_08001198_6B5098(s32 arg0, M2C_UNK arg1) {
    func_08000F74_6B4E74(arg0, func_08001BD8_6B5AD8);
    ((void (*)(s32, s32, f32, s32))func_8022697C_5E1F0C)(arg0, 0, 0.25f, 1);
    ((void (*)(s32, f32))func_8021EB78_5DA108)(arg0, 1.25f);
    ((void (*)(void *))func_80034E8C_35A8C)(func_08001208_6B5108);

    *(volatile int *)0x80000000 = 1;
}
