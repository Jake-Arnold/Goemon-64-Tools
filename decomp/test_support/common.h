#ifndef GOEMON_DECOMP_TEST_TYPES_H
#define GOEMON_DECOMP_TEST_TYPES_H
#include <stdint.h>
typedef uint8_t u8;
typedef int8_t s8;
typedef uint32_t u32;
typedef uint16_t u16;
typedef int16_t s16;
typedef int32_t s32;
typedef float f32;
/* Characterized controller view; native field offsets, not a complete SDK header. */
typedef struct {
    u16 status, button_held_down, button_pressed;
    s16 stick_raw_x, stick_raw_y;
    f32 stick_x, stick_y, stick_magnitude;
} CONTROLLER_W;
/* Synthetic host storage model for memory helpers and VM controller input.
 * Does not copy the upstream SDK/system header or model other engine fields.
 */
typedef struct {
    u8 prefix[0x3ADC0];
    uint16_t fill_color_alpha;
    uint16_t frame_buffer_bits_per_pixel;
    u8 unknown_3ADC4[6];
    u8 retraces_per_game_step;
    u8 unknown_3ADCB;
    u16 retrace_count;
    s16 game_loops_count;
    u8 unknown_3ADD0[4];
    u8 stepw;
    u8 stepw_end;
    u8 unk_3add6, unk_3add7, unk_3add8, unk_3add9;
    u8 unknown_3ADDA[0x3B078 - 0x3ADDA];
    CONTROLLER_W controller[5];
    u8 unknown_after_controller[0xCF8A0 - 0x3B078 - 5*sizeof(CONTROLLER_W)];
    u8 unk_cf8a0;
    u8 remainder[0xCF908 - 0xCF8A1];
} SYS_W;
extern SYS_W D_8008CCC0_8D8C0;
extern SYS_W *D_8015C5C8_15D1C8;
#endif
