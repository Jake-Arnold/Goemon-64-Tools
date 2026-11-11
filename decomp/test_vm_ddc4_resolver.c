/* Host regression for the production DDC4 resolver in script_vm.c.
 * Callback mutation is a deliberate negative control, not retail behavior proof.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#define GOEMON_DECOMP_HOST_TEST 1
#include "script_vm.c"

s32 D_801C78E8_1C84E8;
u16 D_801C78EA_1C84EA;
u16 *D_80077550_78150[1];
u16 D_8007CCA4_7D8A4[1];

static u32 loads[2];
static int load_count;
static int recovery_count;
static int size_count;
static u32 recovery_low;
static u32 size_resource;
static u32 mutate_current_to;
static u32 returned_base;
static u32 returned_segment;
static int retry_first_lookup;

s32 func_800141C4_14DC4(u32 resource) {
    assert(load_count < 2);
    loads[load_count++] = resource;
    if (retry_first_lookup && load_count == 1) {
        return -1;
    }
    return (s32)returned_base;
}

s32 func_80013B14_14714(s32 low_half) {
    recovery_count++;
    recovery_low = (u32)low_half;
    D_801C78E8_1C84E8 = (s32)mutate_current_to;
    return 0;
}

s32 func_80001E50_2A50(u32 resource) {
    size_count++;
    size_resource = resource;
    return (s32)returned_segment;
}

static void reset_mocks(void) {
    loads[0] = loads[1] = 0;
    load_count = recovery_count = size_count = 0;
    recovery_low = size_resource = 0;
    mutate_current_to = 0;
    returned_base = 0;
    returned_segment = 0;
    retry_first_lookup = 0;
}

static u32 expected_address(u32 address, u32 segment, u32 base) {
    return (address - (segment << 24)) + (base & 0xBFFFFFFFu);
}

static void successful_first_lookup(void) {
    const u32 address = 0x1234ABCDu;
    const u32 entry_id = 0x456789ABu;
    const u32 original_current = 0xDEADBEEFu;

    reset_mocks();
    D_801C78E8_1C84E8 = (s32)original_current;
    returned_base = 0xC0009876u;
    returned_segment = 0x12u;
    assert(func_8003DDC4_3E9C4(address, (s32)entry_id) ==
           expected_address(address, returned_segment, returned_base));
    assert(load_count == 1 && loads[0] == entry_id);
    assert(recovery_count == 0 && size_count == 1);
    assert(size_resource == entry_id);
    assert((u32)D_801C78E8_1C84E8 == original_current);
}

static void retry_observes_mutated_current_but_keeps_entry_id(void) {
    static u16 selected[1] = {0x1234};
    const u32 address = 0xF1234567u;
    const u32 entry_id = 0x7ABCDEF0u;
    const u32 remapped_current = 0;
    const u32 initial_current = 0x13572468u;
    const u16 low_half = 0xBEEFu;

    reset_mocks();
    D_801C78E8_1C84E8 = (s32)initial_current;
    D_801C78EA_1C84EA = low_half;
    D_80077550_78150[0] = selected;
    mutate_current_to = remapped_current;
    retry_first_lookup = 1;
    returned_base = 0xC0004444u;
    returned_segment = 0x21u;

    assert(func_8003DDC4_3E9C4(address, (s32)entry_id) ==
           expected_address(address, returned_segment, returned_base));
    assert(load_count == 2);
    assert(loads[0] == entry_id);
    assert(loads[1] == remapped_current);
    assert(recovery_count == 1 && recovery_low == low_half);
    assert(size_count == 1 && size_resource == entry_id);
    assert((u32)D_801C78E8_1C84E8 == remapped_current);
}

int main(void) {
    successful_first_lookup();
    retry_observes_mutated_current_but_keeps_entry_id();
    puts("DDC4 resolver: first-hit and callback-mutation cases passed");
    return 0;
}
