#ifndef HOST_COMMON_H
#define HOST_COMMON_H
#include <stdint.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef int16_t s16;
typedef int32_t s32;
typedef struct { u32 words[2]; } Gfx;
typedef struct { u16 status, button_held_down, button_pressed; s16 stick_raw_x, stick_raw_y; float stick_x, stick_y, stick_magnitude; } CONTROLLER_W;
typedef struct {
    u8 pad0[0x3ADB2];
    s16 current_graphics_pool, file_loader_working_graphics_pool, disable_graphics_tasks;
    u8 pad1[0x12];
    u8 retraces_per_game_step;
    u8 pad2[9];
    u8 stepw, stepw_end, unk_3add6;
    u8 pad3[0x1B];
    u16 intended_room_id, intended_room_group_index;
    u8 pad4[0x22];
    u16 unk_3ae18;
    u8 pad5[0x25E];
    CONTROLLER_W controller[5];
} SYS_W;
void osViSetSpecialFeatures(u32);
#endif
