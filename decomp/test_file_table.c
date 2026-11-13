#include <assert.h>
#ifdef GOEMON_HOST_TEST
#include <stdint.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef int32_t s32;
#else
#include "common.h"
#endif

u32 D_800573D8_57FD8[4] = {0, 0x80000000u, 0xF1234567u, 0x7FFFFFFFu};
u32 func_80001D94_2994(u16);

/* Host reference for G64-071's traced 8-byte entry / bit-30 lookup. */
#define DF4_TEST_WORDS (2u * 65537u)
static u32 df4_test_table[DF4_TEST_WORDS];

static u32 func_80001DF4_29F4_reference(u32 index, u32 type_result) {
    if (type_result == 0x11) {
        return 0x40000000u;
    }
    if (index == 0) {
        return 0;
    }
    return df4_test_table[index * 2] & 0x40000000u;
}

static void test_df4_reference(void) {
    assert(func_80001DF4_29F4_reference(0, 0) == 0);
    assert(func_80001DF4_29F4_reference(1, 0x11) == 0x40000000u);

    df4_test_table[2] = 0x40000000u;
    assert(func_80001DF4_29F4_reference(1, 0x10) == 0x40000000u);
    df4_test_table[2] = 0x80000000u;
    assert(func_80001DF4_29F4_reference(1, 0x10) == 0);
    df4_test_table[2] = 0x20000000u;
    assert(func_80001DF4_29F4_reference(1, 0x10) == 0);
    df4_test_table[2] = 0xC0000000u;
    assert(func_80001DF4_29F4_reference(1, 0x10) == 0x40000000u);

    df4_test_table[2] = 0;
    df4_test_table[3] = 0x40000000u;
    assert(func_80001DF4_29F4_reference(1, 0x10) == 0);

    df4_test_table[2u * 65536u] = 0x40000000u;
    assert(func_80001DF4_29F4_reference(0x00010000u, 0x10) == 0x40000000u);
}

typedef struct {
    u16 boundary;
    u8 unused;
    u8 result;
} de50_test_record;

static u32 func_80001E50_2A50_reference(u32 index, const de50_test_record *records) {
    const de50_test_record *record = records;

    if (index == 0) {
        return 0;
    }
    if (record->boundary == 0) {
        return 0xFF;
    }
    for (;;) {
        if (index < record->boundary) {
            return record->result;
        }
        record++;
        if (record->boundary == 0) {
            return 0xFF;
        }
    }
}

static void test_de50_reference(void) {
    const de50_test_record empty[] = {
        {0, 0xA1, 0xA2},
        {100, 0xA3, 0xA4},
    };
    const de50_test_record limits[] = {
        {0x7FFF, 0xB1, 0x11},
        {0x8000, 0xB2, 0x22},
        {0xFFFF, 0xB3, 0x33},
        {0, 0xB4, 0xB5},
    };
    const de50_test_record sentinel_isolation[] = {
        {2, 0xC1, 0x41},
        {0, 0xC2, 0xC3},
        {100, 0xC4, 0x42},
        {0, 0xC5, 0xC6},
    };

    assert(sizeof(de50_test_record) == 4);
    assert(func_80001E50_2A50_reference(0, empty) == 0);
    assert(func_80001E50_2A50_reference(1, empty) == 0xFF);

    assert(func_80001E50_2A50_reference(1, limits) == 0x11);
    assert(func_80001E50_2A50_reference(0x7FFE, limits) == 0x11);
    assert(func_80001E50_2A50_reference(0x7FFF, limits) == 0x22);
    assert(func_80001E50_2A50_reference(0x8000, limits) == 0x33);
    assert(func_80001E50_2A50_reference(0xFFFE, limits) == 0x33);
    assert(func_80001E50_2A50_reference(0xFFFF, limits) == 0xFF);
    assert(func_80001E50_2A50_reference(0x10000, limits) == 0xFF);
    assert(func_80001E50_2A50_reference(0x80000000u, limits) == 0xFF);
    assert(func_80001E50_2A50_reference(0xFFFFFFFFu, limits) == 0xFF);

    assert(func_80001E50_2A50_reference(1, sentinel_isolation) == 0x41);
    assert(func_80001E50_2A50_reference(3, sentinel_isolation) == 0xFF);
}

typedef struct {
    u32 first_word;
    u32 second_word;
} eb0_test_record;

typedef struct {
    s32 arg0;
    s32 arg1;
    u32 arg2;
    u32 arg3;
    u32 arg4;
    s32 arg5;
} eb0_osmap_call;

static u32 func_80001EB0_2AB0_reference(
    u32 index,
    s32 data,
    u32 reader_result,
    const eb0_test_record *records,
    u32 *mapping_slots,
    eb0_osmap_call *calls,
    u32 *call_count
) {
    u32 first;
    u32 second;
    u32 page_count;
    u32 source_base;
    u32 destination_base;
    u32 offset;
    u32 page;

    *call_count = 0;
    if (reader_result == 0) {
        return 0;
    }

    destination_base = (u32)data & 0x3FFFFFFFu;
    if (index == 0) {
        source_base = 0x07000000u;
        page_count = 31;
    } else {
        first = records[index - 1].first_word;
        second = records[index - 1].second_word;
        page_count = (second - first) >> 13;
        source_base = first;
    }

    for (page = 0, offset = 0; page <= page_count; page++, offset += 0x2000u) {
        u32 destination = destination_base + offset;
        if (mapping_slots[page] == destination) {
            continue;
        }
        mapping_slots[page] = destination;
        calls[*call_count].arg0 = (s32)page;
        calls[*call_count].arg1 = 0;
        calls[*call_count].arg2 = source_base + offset;
        calls[*call_count].arg3 = mapping_slots[page];
        calls[*call_count].arg4 = mapping_slots[page] + 0x1000u;
        calls[*call_count].arg5 = -1;
        (*call_count)++;
    }
    return 0;
}

static void test_eb0_reference(void) {
    const eb0_test_record spans[] = {
        {0x07000000u, 0x07004000u},
    };
    struct {
        u32 before;
        eb0_test_record rows[60];
        u32 after;
    } direct_caller_fixture = {0xA1B2C3D4u, {{0, 0}}, 0x4D3C2B1Au};
    u32 mapping_slots[] = {0, 0x00003000u, 0};
    u32 direct_caller_slots[] = {0};
    eb0_osmap_call calls[3];
    u32 call_count;

    assert(sizeof(eb0_test_record) == 8);
    /* The actual DF4 gate returns zero for index zero, before EB0's fallback. */
    assert(func_80001EB0_2AB0_reference(0, 0x80001000, 0, spans,
                                        mapping_slots, calls, &call_count) == 0);
    assert(call_count == 0);
    assert(mapping_slots[0] == 0);

    /* DF4's nonzero result opens a three-page inclusive range. */
    assert(func_80001EB0_2AB0_reference(1, (s32)0xC0001000u, 0x40000000u, spans,
                                        mapping_slots, calls, &call_count) == 0);
    assert(call_count == 2);
    assert(mapping_slots[0] == 0x00001000u);
    assert(mapping_slots[1] == 0x00003000u);
    assert(mapping_slots[2] == 0x00005000u);
    assert(calls[0].arg0 == 0 && calls[0].arg1 == 0);
    assert(calls[0].arg2 == 0x07000000u && calls[0].arg3 == 0x00001000u);
    assert(calls[0].arg4 == 0x00002000u && calls[0].arg5 == -1);
    assert(calls[1].arg0 == 2 && calls[1].arg1 == 0);
    assert(calls[1].arg2 == 0x07004000u && calls[1].arg3 == 0x00005000u);
    assert(calls[1].arg4 == 0x00006000u && calls[1].arg5 == -1);

    /* Repeating the same request skips every already-correct mapping slot. */
    assert(func_80001EB0_2AB0_reference(1, (s32)0x80001000u, 0x40000000u, spans,
                                        mapping_slots, calls, &call_count) == 0);
    assert(call_count == 0);

    /* The constant caller passes index 60, which selects the 60th row. */
    direct_caller_fixture.rows[59].first_word = 0x07002000u;
    direct_caller_fixture.rows[59].second_word = 0x07002000u;
    assert(func_80001EB0_2AB0_reference(60, (s32)0x80001000u, 0x40000000u,
                                        direct_caller_fixture.rows,
                                        direct_caller_slots, calls, &call_count) == 0);
    assert(call_count == 1);
    assert(calls[0].arg0 == 0 && calls[0].arg2 == 0x07002000u);
    assert(direct_caller_fixture.before == 0xA1B2C3D4u);
    assert(direct_caller_fixture.after == 0x4D3C2B1Au);
}

int main(void) {
    assert(func_80001D94_2994(0) == 0);
    assert(func_80001D94_2994(1) == 0);
    assert(func_80001D94_2994(2) == 0x71234567u);
    assert(func_80001D94_2994(3) == 0x7FFFFFFFu);
    assert(D_800573D8_57FD8[2] == 0xF1234567u);
    test_df4_reference();
    test_de50_reference();
    test_eb0_reference();
    return 0;
}
