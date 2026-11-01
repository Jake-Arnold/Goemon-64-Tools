#ifndef GOEMON_CHECKPOINT_H
#define GOEMON_CHECKPOINT_H
/*
 * Goemon original-game practice checkpoint core.
 * No Win32, recompilation APIs, emulator calls, malloc, filesystem or UI.
 * Intended to be linked into a future N64 ROM patch with a native-memory IO
 * adapter. US ROM symbols only. EXPERIMENTAL and not a full savestate.
 */
#include <stdint.h>

enum { GOEMON_CP_LIVE_SIZE = 0x30, GOEMON_CP_GAMEDATA_SIZE = 0x304,
       GOEMON_CP_HEADER_SIZE = 0x0C };

/* Transfer canonical big-endian guest bytes at 32-bit N64 virtual addresses.
 * On a real N64, memcpy from (volatile uint8_t *)addr is sufficient only when
 * the game is stopped at an appropriate safe point. Do not call asynchronously.
 */
typedef struct {
    void *context;
    int (*read)(void *context, uint32_t n64_addr, void *out, uint32_t length);
    int (*write)(void *context, uint32_t n64_addr, const void *data, uint32_t length);
} GoemonCheckpointIO;

typedef struct {
    uint32_t magic; /* 'GCK1' in host C word representation */
    uint32_t map_id;
    uint32_t character;
    uint32_t object_addr_at_capture; /* INFORMATION ONLY; never restore it */
    uint8_t live[GOEMON_CP_LIVE_SIZE];
    uint8_t gamedata[GOEMON_CP_GAMEDATA_SIZE];
    uint8_t header[GOEMON_CP_HEADER_SIZE];
    uint8_t position[12];
    uint8_t rotation[6];
    uint32_t checksum; /* FNV-1a of bytes before this field */
} GoemonCheckpoint;

/* Returns 0 on success. All other values are intentional failures. */
int goemon_cp_capture(const GoemonCheckpointIO *io, GoemonCheckpoint *out);
int goemon_cp_restore(const GoemonCheckpointIO *io, const GoemonCheckpoint *cp);

#endif
