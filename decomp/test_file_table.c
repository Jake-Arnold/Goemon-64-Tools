#include <assert.h>
#include "common.h"

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

int main(void) {
    assert(func_80001D94_2994(0) == 0);
    assert(func_80001D94_2994(1) == 0);
    assert(func_80001D94_2994(2) == 0x71234567u);
    assert(func_80001D94_2994(3) == 0x7FFFFFFFu);
    assert(D_800573D8_57FD8[2] == 0xF1234567u);
    test_df4_reference();
    test_de50_reference();
    return 0;
}
