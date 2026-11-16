#include "japan_character_switch_prefix_model.h"

#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define BASE 0x80000000u
#define V0 0x80161DC8u
#define S0 0x8016F780u
#define REF 0x80211650u
#define LENGTH 0x300000u

static void set_u32(uint8_t *ram, uint32_t guest, uint32_t value) {
    const uint32_t i = guest - BASE;
    ram[i] = (uint8_t)(value >> 24);
    ram[i+1] = (uint8_t)(value >> 16);
    ram[i+2] = (uint8_t)(value >> 8);
    ram[i+3] = (uint8_t)value;
}

static void assert_u32(const uint8_t *ram, uint32_t guest, uint32_t value) {
    const uint32_t i = guest - BASE;
    assert(ram[i] == (uint8_t)(value >> 24));
    assert(ram[i+1] == (uint8_t)(value >> 16));
    assert(ram[i+2] == (uint8_t)(value >> 8));
    assert(ram[i+3] == (uint8_t)value);
}

int main(void) {
    uint8_t *ram = calloc(LENGTH, 1);
    assert(ram);
    const uint32_t char_byte = S0 + 0x60;
    const uint32_t activation_byte = REF + 0x69;
    set_u32(ram, S0 + 0x5c, REF);

    /* Native trace: object holds 1, caller+callee synchronise the global. */
    ram[char_byte - BASE] = 1;
    assert(jp_character_switch_observed_prefix(ram, LENGTH, V0, S0, 1, 0x11223344) == 0);
    assert_u32(ram, 0x80161DCCu, 1);
    assert_u32(ram, 0x80161DF4u, 0x11223344);
    assert(ram[char_byte - BASE] == 1);
    assert(ram[activation_byte - BASE] == 1);

    /* The callee's byte-derived global store overrides the caller's T9. */
    ram[char_byte - BASE] = 0;
    ram[activation_byte - BASE] = 0;
    assert(jp_character_switch_observed_prefix(ram, LENGTH, V0, S0, 3, 0xAABBCCDD) == 0);
    assert_u32(ram, 0x80161DCCu, 0);
    assert_u32(ram, 0x80161DF4u, 0xAABBCCDD);
    assert(ram[activation_byte - BASE] == 1);

    /* The object is passed in, not hard-coded as one stable gameplay pointer. */
    const uint32_t second_object = 0x80170000u;
    const uint32_t second_indirect = 0x80212000u;
    set_u32(ram, second_object + 0x5c, second_indirect);
    ram[second_object + 0x60 - BASE] = 2;
    assert(jp_character_switch_observed_prefix(ram, LENGTH, V0, second_object, 0, 0) == 0);
    assert_u32(ram, 0x80161DCCu, 2);
    assert(ram[second_indirect + 0x69 - BASE] == 1);

    /* Invalid indirect address is rejected without any guest modifications. */
    uint8_t *saved = malloc(LENGTH);
    assert(saved);
    set_u32(ram, S0 + 0x5c, 0x80300000u);
    memcpy(saved, ram, LENGTH);
    assert(jp_character_switch_observed_prefix(ram, LENGTH, V0, S0, 1, 7) == -1);
    assert(memcmp(saved, ram, LENGTH) == 0);
    assert(jp_character_switch_observed_prefix(ram, LENGTH, V0, 0xFFFFFFFFu, 1, 7) == -1);
    assert(memcmp(saved, ram, LENGTH) == 0);

    free(saved);
    free(ram);
    return 0;
}