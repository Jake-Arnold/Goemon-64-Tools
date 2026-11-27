#include "m2c_types.h"

void func_08000F88_6B0398(s32, void *);
extern u8 func_8003521C_35E1C[];
extern u8 func_80219E08_5D52D8[];
extern u8 func_80221C0C_5DD0DC[];
extern u8 func_0800105C_6B046C[];
extern u8 func_08001EF0_6B1300[];

void func_08001938_6B0D48(s32 arg0, s32 arg1) {
    func_08000F88_6B0398(arg0, func_08001EF0_6B1300);
    ((void (*)(s32, s32, u32, s32))func_80221C0C_5DD0DC)(arg0, 0, 0x3E800000, 1);
    ((void (*)(s32, u32))func_80219E08_5D52D8)(arg0, 0x3FA00000);
    ((void (*)(void *))func_8003521C_35E1C)(func_0800105C_6B046C);
}
