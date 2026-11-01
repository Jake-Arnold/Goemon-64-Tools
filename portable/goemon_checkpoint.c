#include "goemon_checkpoint.h"
#include <stddef.h>
#include <string.h>

#define N64_LIVE      0x8015C5D8u
#define N64_GAMEDATA  0x8015C608u
#define N64_SHADOW    0x8015C910u
#define N64_HEADER    0x8015CC18u
#define N64_MAP       0x800C7AB2u
#define N64_CHARACTER 0x8015C5DCu
#define N64_PLAYEROBJ 0x801FC60Cu
#define MAGIC 0x47434B31u

static uint32_t get32(const uint8_t *b) {
    return ((uint32_t)b[0] << 24) | ((uint32_t)b[1] << 16) |
           ((uint32_t)b[2] << 8) | (uint32_t)b[3];
}
static uint32_t get16(const uint8_t *b) { return ((uint32_t)b[0] << 8) | b[1]; }
static int getbytes(const GoemonCheckpointIO *io, uint32_t a, void *dst, uint32_t sz) {
    return io && io->read && io->read(io->context, a, dst, sz) == 0;
}
static int putbytes(const GoemonCheckpointIO *io, uint32_t a, const void *src, uint32_t sz) {
    return io && io->write && io->write(io->context, a, src, sz) == 0;
}
static int read8(const GoemonCheckpointIO *io, uint32_t a, uint8_t *value) {
    return getbytes(io, a, value, 1);
}
static int safe_gameplay(const GoemonCheckpointIO *io) {
    uint8_t state, phase, exit_req, pause, transferring, event_lock;
    uint8_t loading, submode, vm[4];
    return read8(io, 0x800C7A94u, &state) && state == 13 &&
        read8(io, 0x800C7A9Eu, &phase) && phase == 1 &&
        read8(io, 0x800C7A9Fu, &exit_req) && exit_req == 0 &&
        read8(io, 0x800C7AE6u, &pause) && pause == 0 &&
        read8(io, 0x800C7AD6u, &transferring) && transferring == 0 &&
        read8(io, 0x800C7AE9u, &event_lock) && event_lock == 0 &&
        read8(io, 0x8015C5D4u, &loading) && loading == 0 &&
        read8(io, 0x800C7AA4u, &submode) && submode < 4 && submode != 3 &&
        getbytes(io, 0x80077858u, vm, 4) && get32(vm) == 0;
}
static int identity(const GoemonCheckpointIO *io, uint32_t *map,
                    uint32_t *character, uint32_t *object) {
    uint8_t mapbytes[2], chr[4], obj[4];
    if (!getbytes(io, N64_MAP, mapbytes, 2) ||
        !getbytes(io, N64_CHARACTER, chr, 4) ||
        !getbytes(io, N64_PLAYEROBJ, obj, 4)) return 0;
    *map = get16(mapbytes);
    *character = get32(chr);
    *object = get32(obj);
    return *character < 4 && *object >= 0x80000000u && *object < 0x80800000u;
}
static uint32_t checksum(const GoemonCheckpoint *cp) {
    /* Explicit fields, no padding, deterministic across N64/PC compilers. */
    uint32_t h = 2166136261u, i, j;
    const uint8_t *regions[] = {cp->live, cp->gamedata, cp->header,
                                cp->position, cp->rotation};
    const uint32_t sizes[] = {GOEMON_CP_LIVE_SIZE, GOEMON_CP_GAMEDATA_SIZE,
                              GOEMON_CP_HEADER_SIZE, 12, 6};
    uint32_t ids[] = {cp->magic, cp->map_id, cp->character};
    for (i = 0; i < 3; ++i) for (j = 0; j < 4; ++j) {
        h ^= (ids[i] >> (24 - 8*j)) & 0xFF; h *= 16777619u;
    }
    for (i = 0; i < 5; ++i) for (j = 0; j < sizes[i]; ++j) {
        h ^= regions[i][j]; h *= 16777619u;
    }
    return h;
}
int goemon_cp_capture(const GoemonCheckpointIO *io, GoemonCheckpoint *cp) {
    uint32_t map, chr, obj, map2, chr2, obj2;
    if (!cp || !safe_gameplay(io) || !identity(io, &map, &chr, &obj)) return -1;
    memset(cp, 0, sizeof(*cp));
    cp->magic = MAGIC;
    cp->map_id = map; cp->character = chr; cp->object_addr_at_capture = obj;
    if (!getbytes(io, N64_LIVE, cp->live, GOEMON_CP_LIVE_SIZE) ||
        !getbytes(io, N64_GAMEDATA, cp->gamedata, GOEMON_CP_GAMEDATA_SIZE) ||
        !getbytes(io, N64_HEADER, cp->header, GOEMON_CP_HEADER_SIZE) ||
        !getbytes(io, obj + 8, cp->position, 12) ||
        !getbytes(io, obj + 0x14, cp->rotation, 6)) return -2;
    if (!safe_gameplay(io) || !identity(io, &map2, &chr2, &obj2) ||
        map2 != map || chr2 != chr || obj2 != obj) return -3;
    cp->checksum = checksum(cp);
    return 0;
}
int goemon_cp_restore(const GoemonCheckpointIO *io, const GoemonCheckpoint *cp) {
    uint32_t map, chr, obj;
    uint8_t staged[GOEMON_CP_GAMEDATA_SIZE];
    if (!cp || cp->magic != MAGIC || cp->checksum != checksum(cp)) return -1;
    if (!safe_gameplay(io) || !identity(io, &map, &chr, &obj) ||
        map != cp->map_id || chr != cp->character) return -2;
    /* On real hardware, call at a known frame boundary with the game quiescent.
     * THIS IS NOT ATOMIC and does not recreate live actors or VM context.
     */
    memcpy(staged, cp->gamedata, sizeof(staged));
    memcpy(staged + 0x64, cp->live, GOEMON_CP_LIVE_SIZE);
    if (!putbytes(io, N64_GAMEDATA, staged, sizeof(staged))) return -3;
    if (!putbytes(io, N64_SHADOW, staged, sizeof(staged))) return -4;
    if (!putbytes(io, N64_LIVE, cp->live, GOEMON_CP_LIVE_SIZE)) return -5;
    if (!putbytes(io, N64_HEADER, cp->header, GOEMON_CP_HEADER_SIZE)) return -6;
    if (!putbytes(io, obj + 0x14, cp->rotation, 6)) return -7;
    if (!putbytes(io, obj + 8, cp->position, 12)) return -8;
    return 0;
}
