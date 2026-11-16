#ifndef GOEMON_JP_CHARACTER_SWITCH_PREFIX_MODEL_H
#define GOEMON_JP_CHARACTER_SWITCH_PREFIX_MODEL_H

#include <stddef.h>
#include <stdint.h>

/* Host-only model of the Project64-observed Japanese MIPS stores through
 * 0x801E299C; NOT a recovered whole function, matching C or ROM patch.
 * rdram contains N64 big-endian bytes, indexed from guest 0x80000000.
 * Object and pointed-to region are supplied indirectly, not fixed pointers.
 * Returns 0 on a well-formed captured state, -1 on invalid guest addresses.
 * Invalid calls do not modify the provided memory.
 */
int jp_character_switch_observed_prefix(uint8_t *rdram, size_t rdram_size,
                                        uint32_t caller_v0, uint32_t object_s0,
                                        uint32_t caller_t9, uint32_t caller_t1);

#endif