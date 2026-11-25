#ifndef HOST_COMMON_H
#define HOST_COMMON_H
#include <stdint.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef int16_t s16;
typedef int32_t s32;
typedef struct {
    u8 pad0[0x3ADB6];
    union { s16 field_adb6; s16 disable_graphics_tasks; };
    u8 pad1[0x1C];
    u8 stepw, stepw_end, unk_3add6;
    u8 pad2[0x1D];
    u16 intended_room_group_index;
    u8 pad3[0x22];
    u16 unk_3ae18;
    u8 tail[0xcf908 - 0x3ae1a];
} SYS_W;
#endif
