/* US screen-rectangle bounds setter, ROM 0x222B0. Original symbols retained.
 * Reject invalid input before changing any of the four stored bounds.
 */
#include "common.h"

extern s32 D_8006D158_6DD58;
extern s32 D_8006D15C_6DD5C;
extern s32 D_8006D160_6DD60;
extern s32 D_8006D164_6DD64;

s32 func_800216B0_222B0(s32 left, s32 top, s32 right, s32 bottom) {
    if (left < 0) return 0;
    if (right >= 321) return 0;
    if (top < 0) return 0;
    if (bottom >= 241) return 0;
    if (right < left) return 0;
    if (bottom < top) return 0;
    D_8006D158_6DD58 = left;
    D_8006D15C_6DD5C = top;
    D_8006D160_6DD60 = right;
    D_8006D164_6DD64 = bottom;
    return 1;
}
