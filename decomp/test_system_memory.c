/* Host-only boundary/overlap/init tests, never actual system/game RAM. */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include "common.h"

SYS_W D_8008CCC0_8D8C0;
SYS_W *D_8015C5C8_15D1C8;
u8 D_8015C5D4_15D1D4;
void func_80004170_4D70(void);
void func_800041E0_4DE0(u8 *, s32);
void func_80004208_4E08(u8 *, u8 *, s32);

_Static_assert(sizeof(SYS_W) == 0xCF908, "Synthetic system size");
_Static_assert(offsetof(SYS_W, fill_color_alpha) == 0x3ADC0, "Alpha offset");
_Static_assert(offsetof(SYS_W, frame_buffer_bits_per_pixel) == 0x3ADC2, "Framebuffer field offset");

int main(void) {
    u8 source[4100], target[4100], original[4100], overlap[16];
    const s32 lengths[] = {0, 1, 2, 3, 63, 64, 100, 255, 4096};
    unsigned trial, i;
    static SYS_W expected;
    func_800041E0_4DE0(NULL, 0);
    func_80004208_4E08(NULL, NULL, 0);
    for (trial = 0; trial < sizeof(lengths) / sizeof(lengths[0]); trial++) {
        s32 count = lengths[trial];
        memset(target, 0xA5, sizeof(target));
        func_800041E0_4DE0(target + 3, count);
        for (i = 0; i < sizeof(target); i++) assert(target[i] == (i >= 3 && i < 3 + (unsigned)count ? 0 : 0xA5));
        for (i = 0; i < sizeof(source); i++) source[i] = (u8)(i * 7);
        memcpy(original, source, sizeof(source));
        memset(target, 0xA5, sizeof(target));
        func_80004208_4E08(source + 1, target + 3, count);
        for (i = 0; i < sizeof(target); i++) assert(target[i] == (i >= 3 && i < 3 + (unsigned)count ? source[i - 2] : 0xA5));
        assert(memcmp(source, original, sizeof(source)) == 0);
    }
    for (i = 0; i < sizeof(overlap); i++) overlap[i] = (u8)i;
    func_80004208_4E08(overlap, overlap + 1, 8);
    for (i = 1; i <= 8; i++) assert(overlap[i] == 0); /* Forward byte copy, not memmove. */
    for (i = 0; i < sizeof(overlap); i++) overlap[i] = (u8)i;
    func_80004208_4E08(overlap + 1, overlap, 8);
    for (i = 0; i < 8; i++) assert(overlap[i] == i + 1);
    memcpy(original, overlap, sizeof(overlap));
    func_80004208_4E08(overlap, overlap, sizeof(overlap));
    assert(memcmp(original, overlap, sizeof(overlap)) == 0);
    memset(&D_8008CCC0_8D8C0, 0xA5, sizeof(D_8008CCC0_8D8C0));
    D_8015C5C8_15D1C8 = NULL;
    D_8015C5D4_15D1D4 = 0xA5;
    func_80004170_4D70();
    memset(&expected, 0, sizeof(expected));
    expected.fill_color_alpha = 1;
    expected.frame_buffer_bits_per_pixel = 2;
    assert(D_8015C5C8_15D1C8 == &D_8008CCC0_8D8C0);
    assert(D_8015C5D4_15D1D4 == 0);
    assert(memcmp(&expected, &D_8008CCC0_8D8C0, sizeof(expected)) == 0);
    puts("System initialization, zero/copy boundaries and forward-overlap semantics passed.");
    return 0;
}
