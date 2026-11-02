/* Reconstructed system initialization and byte-memory primitives, US ROM 0x4D70. */
#include "common.h"

extern u8 D_8015C5D4_15D1D4;

void func_800041E0_4DE0(u8 *destination, s32 length);

void func_80004170_4D70(void) {
    func_800041E0_4DE0((u8 *)&D_8008CCC0_8D8C0, 0xCF908);
    D_8015C5C8_15D1C8 = &D_8008CCC0_8D8C0;
    D_8015C5D4_15D1D4 = 0;
    D_8015C5C8_15D1C8->fill_color_alpha = 1;
    D_8015C5C8_15D1C8->frame_buffer_bits_per_pixel = 2;
}

void func_800041E0_4DE0(u8 *destination, s32 length) {
    while (length--) {
        *destination++ = 0;
    }
}

void func_80004208_4E08(u8 *source, u8 *destination, s32 length) {
    while (length--) {
        *destination++ = *source++;
    }
}
