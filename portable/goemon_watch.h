#ifndef GOEMON_WATCH_H
#define GOEMON_WATCH_H
/* Pure C logical game-state inspector for original USA N64 game.
 * Read-only, no allocations, no host OS or N64Recomp dependency.
 * Uses same guest-byte read callback as checkpoint core.
 */
#include <stdint.h>
#include "goemon_checkpoint.h"
typedef struct {
    uint32_t character;
    uint32_t max_hp, current_hp, ryo, lives;
    uint16_t map_id;
    uint8_t top_state, phase, loading;
    uint8_t item_slots[3];
    uint8_t party[4];
    uint8_t weapon_upgrades[4];
    uint8_t optional_items[4]; /* chain pipe, hammer, bomb, flute */
    uint32_t warnings; /* bit 0 char, bit 1 health, bit 2 ryo, bit 3 lives */
} GoemonWatch;

/* Returns zero on complete read. Never writes. */
int goemon_watch_read(const GoemonCheckpointIO *io, GoemonWatch *out);

#endif
