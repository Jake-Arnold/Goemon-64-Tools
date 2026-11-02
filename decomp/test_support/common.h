#ifndef GOEMON_DECOMP_TEST_TYPES_H
#define GOEMON_DECOMP_TEST_TYPES_H
#include <stdint.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef int16_t s16;
typedef int32_t s32;
/* Synthetic host storage model for the fields accessed by system_memory.c.
 * Does not copy the upstream SDK/system header or model other engine fields.
 */
typedef struct {
    u8 prefix[0x3ADC0];
    uint16_t fill_color_alpha;
    uint16_t frame_buffer_bits_per_pixel;
    u8 unknown_3ADC4[8];
    u16 retrace_count;
    u8 unknown_3ADCE[0xCF8A0 - 0x3ADCE];
    u8 unk_cf8a0;
    u8 remainder[0xCF908 - 0xCF8A1];
} SYS_W;
extern SYS_W D_8008CCC0_8D8C0;
extern SYS_W *D_8015C5C8_15D1C8;
#endif
