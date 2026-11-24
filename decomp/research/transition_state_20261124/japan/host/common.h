#ifndef HOST_COMMON_H
#define HOST_COMMON_H
#include <stdint.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef int32_t s32;
/* Semantic fixture: these fields are independent in host memory; target offsets
 * are verified separately by the original-ROM native byte comparison. */
typedef struct {
    u8 stepw, stepw_end, retraces_per_game_step;
    u8 unk_3add6, unk_3add7, unk_3add8, unk_3add9;
    u8 unk_3adde, unk_3addf, unk_3ade0, unk_3ade1;
    u16 intended_room_group_index, unk_3ae18;
    u8 unk_3b01d;
    /* Host-only space for the static-base +0x30000 view; not an ABI proof. */
    u8 storage[0x3B020];
} SYS_W;
#endif
