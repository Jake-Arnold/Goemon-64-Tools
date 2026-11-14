#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

uint8_t engine_reset_fixture[5] = {0x34, 0x12, 0x56, 0x78, 0x9A};
uint8_t engine_flags_fixture[4] = {0x22, 0xA0, 0x00, 0xB5};

__asm__(
    ".globl D_801C09D8_1C15D8\n"
    ".set D_801C09D8_1C15D8, engine_reset_fixture\n"
    ".globl D_801C09DA_1C15DA\n"
    ".set D_801C09DA_1C15DA, engine_reset_fixture+2\n"
    ".globl D_801C09DB_1C15DB\n"
    ".set D_801C09DB_1C15DB, engine_reset_fixture+3\n"
    ".globl D_801C09DC_1C15DC\n"
    ".set D_801C09DC_1C15DC, engine_reset_fixture+4\n"
    ".globl D_801C09CE_1C15CE\n"
    ".set D_801C09CE_1C15CE, engine_flags_fixture\n"
    ".globl D_801C09CF_1C15CF\n"
    ".set D_801C09CF_1C15CF, engine_flags_fixture+1\n"
    ".globl D_801C09D0_1C15D0\n"
    ".set D_801C09D0_1C15D0, engine_flags_fixture+2\n"
    ".globl D_801C09D1_1C15D1\n"
    ".set D_801C09D1_1C15D1, engine_flags_fixture+3\n");

enum {
    FLAG_CE = 0,
    FLAG_CF = 1,
    FLAG_D0 = 2,
    FLAG_D1 = 3,
    PAN_ENTRY_COUNT = 16,
    PAN_ENTRY_STRIDE = 0xB0,
    PAN_TARGET_STRIDE = 0x1C
};

typedef struct {
    uint32_t object_word;
    uint8_t reserved_04_05[2];
    uint8_t flags;
    uint8_t reserved_07_57[0x51];
    uint16_t pan_word;
    uint8_t reserved_5A_AF[0x56];
} PanEntry;

typedef struct {
    uint32_t alignment_word;
    uint8_t bytes[PAN_TARGET_STRIDE - sizeof(uint32_t)];
} PanTarget;

_Static_assert(offsetof(PanEntry, object_word) == 0, "entry object word offset");
_Static_assert(offsetof(PanEntry, flags) == 0x06, "entry flags offset");
_Static_assert(offsetof(PanEntry, pan_word) == 0x58, "entry pan offset");
_Static_assert(sizeof(PanEntry) == PAN_ENTRY_STRIDE, "entry stride");
_Static_assert(sizeof(PanTarget) == PAN_TARGET_STRIDE, "pan target stride");

typedef struct {
    PanEntry entries[PAN_ENTRY_COUNT];
    PanTarget targets[PAN_ENTRY_COUNT];
    PanEntry *current_entry;
    uint32_t audio_context;
    size_t slot_writes;
    size_t call_count;
    size_t call_indices[PAN_ENTRY_COUNT];
    int call_pans[PAN_ENTRY_COUNT];
    int callback_rearms_latch;
} PanSweepFixture;

static PanSweepFixture pan_sweep;

void func_80039F3C_3AB3C(void);
void func_80039F60_3AB60(void);
void func_8003A1E8_3ADE8(void);

/* MIPS-derived host reference only; production 80039F84 remains GLOBAL_ASM. */
static void mock_alSynSetPan(uint32_t context, PanTarget *target, int pan) {
    size_t index = (size_t)(target - &pan_sweep.targets[0]);

    assert(context == pan_sweep.audio_context);
    assert(index < PAN_ENTRY_COUNT);
    assert(pan_sweep.current_entry == &pan_sweep.entries[index]);
    assert(pan_sweep.entries[index].object_word != 0);
    assert((pan_sweep.entries[index].flags & 1) != 0);
    assert(pan_sweep.call_count < PAN_ENTRY_COUNT);
    if (pan_sweep.call_count == 0) {
        assert(engine_flags_fixture[FLAG_D0] == 0);
    } else if (pan_sweep.callback_rearms_latch) {
        assert(engine_flags_fixture[FLAG_D0] == 0xA5);
    }

    pan_sweep.call_indices[pan_sweep.call_count] = index;
    pan_sweep.call_pans[pan_sweep.call_count] = pan;
    pan_sweep.call_count++;

    if (pan_sweep.callback_rearms_latch) {
        engine_flags_fixture[FLAG_D0] = 0xA5;
    }
}

static void reference_func_80039F84(void) {
    size_t index;

    if (engine_flags_fixture[FLAG_D0] == 0) {
        return;
    }

    engine_flags_fixture[FLAG_D0] = 0;
    for (index = 0; index < PAN_ENTRY_COUNT; index++) {
        PanEntry *entry = &pan_sweep.entries[index];
        uint8_t *pan_target = (uint8_t *)&pan_sweep.targets[0] +
                              index * PAN_TARGET_STRIDE;
        uint8_t high_pan;

        pan_sweep.current_entry = entry;
        pan_sweep.slot_writes++;
        if (entry->object_word == 0) {
            continue;
        }

        entry->flags |= 1;
        high_pan = (uint8_t)(entry->pan_word >> 8);
        mock_alSynSetPan(pan_sweep.audio_context,
                         (PanTarget *)pan_target,
                         high_pan & 0x7F);
    }
}

static void reset_pan_fixture(void) {
    memset(&pan_sweep, 0, sizeof(pan_sweep));
    pan_sweep.audio_context = UINT32_C(0x12345678);
    engine_flags_fixture[FLAG_CE] = 0xD3;
    engine_flags_fixture[FLAG_CF] = 0x4A;
    engine_flags_fixture[FLAG_D0] = 0;
    engine_flags_fixture[FLAG_D1] = 0xB5;
}

static void test_matched_ce_cf_helpers(void) {
    uint8_t d0 = 0x36;
    uint8_t d1 = 0xC7;

    engine_flags_fixture[FLAG_CE] = 0x22;
    engine_flags_fixture[FLAG_CF] = 0xA0;
    engine_flags_fixture[FLAG_D0] = d0;
    engine_flags_fixture[FLAG_D1] = d1;
    func_80039F3C_3AB3C();
    assert(engine_flags_fixture[FLAG_CE] == 0x22);
    engine_flags_fixture[FLAG_CF] = 0xA1;
    func_80039F3C_3AB3C();
    assert(engine_flags_fixture[FLAG_CE] == 0xFF);
    assert(engine_flags_fixture[FLAG_CF] == 0xA1);

    engine_flags_fixture[FLAG_CE] = 0x40;
    engine_flags_fixture[FLAG_CF] = 0;
    func_80039F60_3AB60();
    assert(engine_flags_fixture[FLAG_CE] == 0x40);
    engine_flags_fixture[FLAG_CF] = 1;
    func_80039F60_3AB60();
    assert(engine_flags_fixture[FLAG_CE] == 1);
    assert(engine_flags_fixture[FLAG_D0] == d0);
    assert(engine_flags_fixture[FLAG_D1] == d1);
}

static void test_zero_latch_is_noop(void) {
    PanEntry *previous_entry;
    uint8_t flags_before[4];

    reset_pan_fixture();
    previous_entry = &pan_sweep.entries[3];
    pan_sweep.current_entry = previous_entry;
    engine_flags_fixture[FLAG_D0] = 0;
    memcpy(flags_before, engine_flags_fixture, sizeof(flags_before));

    reference_func_80039F84();

    assert(pan_sweep.current_entry == previous_entry);
    assert(pan_sweep.slot_writes == 0);
    assert(pan_sweep.call_count == 0);
    assert(memcmp(flags_before, engine_flags_fixture, sizeof(flags_before)) == 0);
}

static void test_nonzero_latch_with_empty_entries(void) {
    reset_pan_fixture();
    engine_flags_fixture[FLAG_CE] = 0x81;
    engine_flags_fixture[FLAG_CF] = 0xA0;
    engine_flags_fixture[FLAG_D0] = 7;
    engine_flags_fixture[FLAG_D1] = 0x5E;
    pan_sweep.current_entry = NULL;

    reference_func_80039F84();

    assert(engine_flags_fixture[FLAG_D0] == 0);
    assert(engine_flags_fixture[FLAG_CE] == 0x81);
    assert(engine_flags_fixture[FLAG_CF] == 0xA0);
    assert(engine_flags_fixture[FLAG_D1] == 0x5E);
    assert(pan_sweep.slot_writes == PAN_ENTRY_COUNT);
    assert(pan_sweep.call_count == 0);
    assert(pan_sweep.current_entry == &pan_sweep.entries[PAN_ENTRY_COUNT - 1]);
}

static void test_active_entry_pan_sweep(void) {
    static const size_t active_indices[] = {0, 5, 10, 15};
    static const uint16_t pan_words[] = {0x0000, 0x7F00, 0x8000, 0xFF00};
    static const int expected_pan[] = {0, 0x7F, 0, 0x7F};
    static const uint8_t initial_flags[] = {0x40, 0x80, 0xFE, 0x02};
    size_t active;

    reset_pan_fixture();
    engine_flags_fixture[FLAG_CE] = 0xE2;
    engine_flags_fixture[FLAG_CF] = 0xA0;
    engine_flags_fixture[FLAG_D0] = 3;
    engine_flags_fixture[FLAG_D1] = 0x79;

    for (active = 0; active < sizeof(active_indices) / sizeof(active_indices[0]); active++) {
        size_t index = active_indices[active];
        pan_sweep.entries[index].object_word = index == 10
                                                   ? UINT32_C(0x80000000)
                                                   : (uint32_t)(index + 1);
        pan_sweep.entries[index].flags = initial_flags[active];
        pan_sweep.entries[index].pan_word = pan_words[active];
    }
    pan_sweep.entries[1].flags = 0x80;
    pan_sweep.entries[14].flags = 0x55;
    pan_sweep.callback_rearms_latch = 1;

    reference_func_80039F84();

    assert(engine_flags_fixture[FLAG_D0] == 0xA5);
    assert(engine_flags_fixture[FLAG_CE] == 0xE2);
    assert(engine_flags_fixture[FLAG_CF] == 0xA0);
    assert(engine_flags_fixture[FLAG_D1] == 0x79);
    assert(pan_sweep.slot_writes == PAN_ENTRY_COUNT);
    assert(pan_sweep.call_count == sizeof(active_indices) / sizeof(active_indices[0]));
    assert(pan_sweep.current_entry == &pan_sweep.entries[PAN_ENTRY_COUNT - 1]);

    for (active = 0; active < pan_sweep.call_count; active++) {
        size_t index = active_indices[active];
        assert(pan_sweep.call_indices[active] == index);
        assert(pan_sweep.call_pans[active] == expected_pan[active]);
        assert(pan_sweep.entries[index].flags == (uint8_t)(initial_flags[active] | 1));
    }
    assert(pan_sweep.entries[1].flags == 0x80);
    assert(pan_sweep.entries[14].flags == 0x55);
}

int main(void) {
    func_8003A1E8_3ADE8();
    assert(engine_reset_fixture[0] == 0);
    assert(engine_reset_fixture[1] == 0);
    assert(engine_reset_fixture[2] == 0);
    assert(engine_reset_fixture[3] == 0x78);
    assert(engine_reset_fixture[4] == 0x9A);

    test_matched_ce_cf_helpers();
    test_zero_latch_is_noop();
    test_nonzero_latch_with_empty_entries();
    test_active_entry_pan_sweep();
    return 0;
}
