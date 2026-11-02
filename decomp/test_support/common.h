#ifndef GOEMON_DECOMP_TEST_TYPES_H
#define GOEMON_DECOMP_TEST_TYPES_H
#include <stdint.h>
typedef uint8_t u8;
typedef int32_t s32;
/* Synthetic host storage model for the fields accessed by system_memory.c.
 * Does not copy the upstream SDK/system header or model other engine fields.
 */
typedef struct {
    u8 prefix[0x3ADC0];
    uint16_t fill_color_alpha;
    uint16_t frame_buffer_bits_per_pixel;
    u8 remainder[0xCF908 - 0x3ADC4];
} SYS_W;
extern SYS_W D_8008CCC0_8D8C0;
extern SYS_W *D_8015C5C8_15D1C8;
#endif
