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

int main(void) {
    assert(func_80001D94_2994(0) == 0);
    assert(func_80001D94_2994(1) == 0);
    assert(func_80001D94_2994(2) == 0x71234567u);
    assert(func_80001D94_2994(3) == 0x7FFFFFFFu);
    assert(D_800573D8_57FD8[2] == 0xF1234567u);
    test_df4_reference();
    return 0;
}
