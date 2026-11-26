/* Reconstructed from the verified US ROM, translation unit ROM 0x249F0.
 * Original symbol names retained for comparison with pinned mnsg.
 * These are unchecked engine routines, not public safe editing APIs.
 */
#include "common.h"

extern u8 D_80161DF8_1629F8[];
extern u8 D_80168EF4_169AF4[];
extern u8 D_80168EF8_169AF8[];
extern u8 D_80168F5C_169B5C[];
extern u8 D_8015C608_15D208[];
extern u8 D_8015C66C_15D26C[];

s32 func_80023D9C_2499C(s32 flag) {
    { *(volatile int *)0x80000000 = 1; } return D_80161DF8_1629F8[(u8)(flag / 8)] & ((u8)(1 << (u8)(flag % 8))) & 0xFF;
}
