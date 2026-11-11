/* Synthetic regression: recovery callbacks may rewrite the resource ID.
 * The original loader reloads it for recovery/size callbacks, but retains
 * the entry argument for the later offset/delta callback. Not in-game proof.
 */
#include <assert.h>
#include <stdint.h>
#include <string.h>
#define GOEMON_DECOMP_HOST_TEST 1
#include "candidates/vm_loader_storage_probe.c"

void *D_80077860_78460;
s32 D_8007785C_7845C, D_80077858_78458;
VmResourceContext D_801C78E8_1C84E8;
VmWorkLoader D_801C77E8_1C83E8;
s32 D_801C7900_1C8500, D_801C7904_1C8504;
s32 D_801C7740_1C8340,D_801C7744_1C8344,D_801C7748_1C8348,D_801C774C_1C834C;
s32 D_801C7750_1C8350,D_801C7754_1C8354,D_801C7758_1C8358,D_801C775C_1C835C;
s32 D_801C7760_1C8360,D_801C7764_1C8364,D_801C7768_1C8368,D_801C776C_1C836C;
s32 D_801C7770_1C8370,D_801C7774_1C8374,D_801C7798_1C8398,D_801C77A0_1C83A0;
s32 D_801C77D8_1C83D8,D_801C77E0_1C83E0;
s32 D_801C78D0_1C84D0,D_801C78FC_1C84FC;
s32 D_801C7920_1C8520,D_801C7924_1C8524,D_801C7928_1C8528,D_801C792C_1C852C;

static s32 first_remap, second_remap, seen_load[2], seen_reset, seen_size, seen_delta;
static int load_count, restore_count, reset_count, size_count, delta_count, init_count, state_count;
static u16 recovered_low;

s32 func_800141C4_14DC4(s32 id) {
    assert(load_count < 2);
    seen_load[load_count++] = id;
    return load_count == 1 ? -1 : (s32)0xC0001234u;
}
void func_80013B14_14714(u16 id) {
    restore_count++;
    recovered_low = id;
    D_801C78E8_1C84E8.current_id.word = first_remap;
}
void func_8003CFA0_3DBA0(s32 id) {
    reset_count++;
    seen_reset = id;
    D_801C78E8_1C84E8.current_id.word = second_remap;
}
s32 func_80001E50_2A50(s32 id) { size_count++; seen_size = id; return id ^ 0x51A55A1; }
s32 func_8003DDC4_3E9C4(s32 start, s32 id) {
    delta_count++; seen_delta = id; return start + 0x34;
}
s32 func_8003DE48_3EA48(s32 start) { init_count++; return start + 5; }
void func_80024088_24C88(s32 code) { assert(code == 0x82); state_count++; }

static void one_case(s32 entry, s32 first, s32 second, s32 start) {
    u8 owner[0x60];
    memset(owner, 0x77, sizeof(owner));
    D_80077860_78460 = owner;
    first_remap = first;
    second_remap = second;
    load_count = restore_count = reset_count = size_count = delta_count = init_count = state_count = 0;
    recovered_low = 0;
    assert(entry != -1 && first != entry && second != first && second != entry);
    assert(func_8003D468_3E068(start, entry) == 1);
    assert(load_count == 2 && seen_load[0] == entry && seen_load[1] == second);
    assert(restore_count == 1 && recovered_low == (u16)entry);
    assert(reset_count == 1 && seen_reset == first);
    assert(size_count == 1 && seen_size == second);
    assert(delta_count == 1 && seen_delta == entry);
    assert(init_count == 1 && state_count == 1);
    assert((s32)D_801C78E8_1C84E8.current_id.word == second);
    assert(D_801C78E8_1C84E8.unknown_04 == (second ^ 0x51A55A1));
    assert(D_801C78E8_1C84E8.unknown_08 == 0x34);
    assert(D_801C77E8_1C83E8.loaded == (s32)0x80001234u);
    assert(D_80077858_78458 == start + 5);
    assert(D_801C77E8_1C83E8.marker == -1 && D_801C77E8_1C83E8.gate == 0);
    assert(D_801C77D8_1C83D8 == 1 && D_801C77E0_1C83E0 == 0);
    assert(owner[0x5c] == 0 && owner[0x5d] == 0);
}

int main(void) {
    unsigned int seed = 0x3E068u;
    for (int i = 0; i < 1024; ++i) {
        seed = seed * 1664525u + 1013904223u;
        s32 entry = (s32)(0x10000000u | (seed & 0x0FFFFFFFu));
        s32 first = (s32)(0x20000000u | (seed & 0x0FFFFFFFu));
        s32 second = (s32)(0x30000000u | (seed & 0x0FFFFFFFu));
        one_case(entry, first, second, i + 10);
    }
    return 0;
}
