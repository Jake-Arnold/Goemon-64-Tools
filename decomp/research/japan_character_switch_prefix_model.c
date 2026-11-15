#include "japan_character_switch_prefix_model.h"

#define GUEST_KSEG0 0x80000000u
#define CHARACTER_INDEX_GLOBAL 0x80161DCCu

/* A bounded guest-byte adapter, not the game's native pointer implementation. */
static int guest_offset(size_t size, uint64_t guest, size_t bytes, size_t *offset) {
    if (guest < GUEST_KSEG0 || guest - GUEST_KSEG0 > SIZE_MAX) {
        return 0;
    }
    const size_t index = (size_t)(guest - GUEST_KSEG0);
    if (index > size || bytes > size - index) {
        return 0;
    }
    *offset = index;
    return 1;
}

static uint32_t read_be32(const uint8_t *memory) {
    return ((uint32_t)memory[0] << 24) | ((uint32_t)memory[1] << 16) |
           ((uint32_t)memory[2] << 8) | (uint32_t)memory[3];
}

static void write_be32(uint8_t *memory, uint32_t value) {
    memory[0] = (uint8_t)(value >> 24);
    memory[1] = (uint8_t)(value >> 16);
    memory[2] = (uint8_t)(value >> 8);
    memory[3] = (uint8_t)value;
}

int jp_character_switch_observed_prefix(uint8_t *rdram, size_t rdram_size,
                                        uint32_t caller_v0, uint32_t object_s0,
                                        uint32_t caller_t9, uint32_t caller_t1) {
    size_t caller_index, caller_secondary, object_pointer_word, object_character;
    size_t callee_global, indirect_character_byte;
    if (rdram == NULL ||
        !guest_offset(rdram_size, (uint64_t)caller_v0 + 4, 4, &caller_index) ||
        !guest_offset(rdram_size, (uint64_t)caller_v0 + 0x2c, 4, &caller_secondary) ||
        !guest_offset(rdram_size, (uint64_t)object_s0 + 0x5c, 4, &object_pointer_word) ||
        !guest_offset(rdram_size, (uint64_t)object_s0 + 0x60, 1, &object_character) ||
        !guest_offset(rdram_size, CHARACTER_INDEX_GLOBAL, 4, &callee_global)) {
        return -1;
    }
    const uint32_t pointed_to = read_be32(rdram + object_pointer_word);
    if (!guest_offset(rdram_size, (uint64_t)pointed_to + 0x69, 1,
                      &indirect_character_byte)) {
        return -1;
    }

    /* Caller: 801E2944, 801E2948, 801E294C. */
    write_be32(rdram + caller_index, caller_t9);
    write_be32(rdram + caller_secondary, caller_t1);
    const uint8_t a1 = rdram[object_character];
    /* 801E2950/2954: JAL with A0=S0; then callee through 801E299C. */
    rdram[object_character] = a1;                    /* SB a2, 0x60(a0) */
    write_be32(rdram + callee_global, (uint32_t)a1); /* ANDI, SW global */
    rdram[indirect_character_byte] = 1;             /* SB 1, 0x69(t7) */
    /* The MTC1 F0=0 and all later instructions/callers remain unresolved. */
    return 0;
}