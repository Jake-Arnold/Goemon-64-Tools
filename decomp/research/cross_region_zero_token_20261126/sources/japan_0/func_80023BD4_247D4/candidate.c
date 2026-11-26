/* Reconstructed from the verified US ROM, translation unit ROM 0x249F0.
 * Original symbol names retained for comparison with pinned mnsg.
 * These are unchecked engine routines, not public safe editing APIs.
 */
#include "common.h"

extern u8 D_8016E6D8_16F2D8[];
extern u8 D_80168EF4_169AF4[];
extern u8 D_80168EF8_169AF8[];
extern u8 D_80168F5C_169B5C[];
extern u8 D_8015C608_15D208[];
extern u8 D_8015C66C_15D26C[];

void func_80023BD4_247D4(s32 flag) {
    u8 *byte;
    byte = D_8016E6D8_16F2D8 + (u8)(flag / 8);
    *byte |= (u8)(1 << (u8)(flag % 8));
}
