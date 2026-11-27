#include "m2c_types.h"

void func_80004240_4E40(void);
void func_80014B74_15774(void *, s32);
extern u8 D_3ADDF[];
extern u8 *D_8015C5C8_15D1C8;
extern s32 D_8020EED0_63A2B0;

void func_801CB5C0_5F69A0(void) {
    func_80004240_4E40();
    func_80014B74_15774(D_8015C5C8_15D1C8 + 0xC7FA4, D_8020EED0_63A2B0);
    D_8015C5C8_15D1C8[(u32)D_3ADDF] = 1;
}
