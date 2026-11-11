/* Host checks for the confirmed VM resource record widths and N64 byte order. */
#define GOEMON_DECOMP_HOST_TEST 1
#include "vm_resource_types.h"
#include <assert.h>
#include <stddef.h>

_Static_assert(sizeof(VmResourceId) == 4, "resource ID is one word");
_Static_assert(offsetof(VmResourceId, word) == 0, "word starts at +0");
_Static_assert(offsetof(VmResourceId, n64_be.high_half) == 0, "big-endian high half is +0");
_Static_assert(offsetof(VmResourceId, n64_be.low_half) == 2, "big-endian low half is +2");
_Static_assert(sizeof(VmResourceContext) == 12, "resource context spans +0 through +B");
_Static_assert(offsetof(VmResourceContext, current_id) == 0, "current ID is +0");
_Static_assert(offsetof(VmResourceContext, unknown_04) == 4, "unknown word is +4");
_Static_assert(offsetof(VmResourceContext, unknown_08) == 8, "unknown word is +8");

int main(void) {
    static const u32 words[] = {0x12345678, 0xFFFFFFFF, 0x0000ABCD, 0x9ABC0001};
    static const u16 lows[] = {0x5678, 0xFFFF, 0xABCD, 0x0001};
    size_t i;

    for (i = 0; i < sizeof(words) / sizeof(words[0]); ++i) {
        VmResourceId id;
        const u8 n64_big_endian_word[4] = {
            (u8)(words[i] >> 24), (u8)(words[i] >> 16),
            (u8)(words[i] >> 8), (u8)words[i]
        };

        id.word = words[i];
        assert(VM_RESOURCE_ID_LOW_HALF(id) == lows[i]);
        assert((((u16)n64_big_endian_word[2] << 8) | n64_big_endian_word[3]) ==
               VM_RESOURCE_ID_LOW_HALF(id));
    }
    return 0;
}
