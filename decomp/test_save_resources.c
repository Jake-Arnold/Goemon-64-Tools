/* Synthetic host test. GNU symbol aliases model overlapping guest save views. */
#define GOEMON_DECOMP_HOST_TEST
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include "save_resources.c"

SaveData D_8015C608_15D208;
SaveData D_8015C910_15D510;
ResourceBlock D_8015C5D8_15D1D8;
SYS_W D_8008CCC0_8D8C0;
SYS_W *D_8015C5C8_15D1C8 = &D_8008CCC0_8D8C0;
u8 D_8015C5D4_15D1D4;
s32 D_80167C48_168848[3];
s32 D_80167C54_168854;
static s32 calls[3], call_count;

__asm__(".globl D_8015C66C_15D26C\n.set D_8015C66C_15D26C, D_8015C608_15D208 + 100\n"
        ".globl D_8015C698_15D298\n.set D_8015C698_15D298, D_8015C608_15D208 + 144\n"
        ".globl D_800BCCC0_BD8C0\n.set D_800BCCC0_BD8C0, D_8008CCC0_8D8C0 + 196608\n");

void func_8000B8F0_C4F0(s32 index) { assert(call_count < 3); calls[call_count++] = index; }

_Static_assert(sizeof(SaveData) == 0x304, "Save size");
_Static_assert(sizeof(ResourceBlock) == 0x30, "Resource size");
_Static_assert(offsetof(SaveData, resources) == 0x64, "Saved resource view");
_Static_assert(offsetof(SaveData, resources.word_2C) == 0x90, "Saved mode alias");
_Static_assert(offsetof(SaveData, word_FC) == 0xFC, "Health-upgrade count");
_Static_assert(offsetof(SaveData, half_204) == 0x204, "Saved map");
_Static_assert(offsetof(SaveData, word_264) == 0x264, "Played seconds");
_Static_assert(offsetof(SaveData, word_29C) == 0x29C, "Counter offset");
_Static_assert(offsetof(TimerView, ticks) + 0x30000 == offsetof(SYS_W, retrace_count), "Timer alias");

static void check_buffer_views(void) {
    SaveData expected;
    ResourceBlock expected_live;
    memset(&D_8015C608_15D208, 0x45, sizeof(SaveData));
    D_8015C608_15D208.resources.word_00 = 77;
    D_8015C608_15D208.resources.word_2C = 99;
    D_8008CCC0_8D8C0.unk_cf8a0 = 7;
    expected = D_8015C608_15D208;
    expected.resources.word_2C = 1;
    expected_live = expected.resources;
    expected_live.word_00 = 1;
    func_8000B5D0_C1D0();
    assert(D_8008CCC0_8D8C0.unk_cf8a0 == 0);
    assert(memcmp(&expected, &D_8015C608_15D208, sizeof(expected)) == 0);
    assert(memcmp(&expected, &D_8015C910_15D510, sizeof(expected)) == 0);
    assert(memcmp(&expected_live, &D_8015C5D8_15D1D8, sizeof(expected_live)) == 0);
    memset(&D_8015C910_15D510, 0x36, sizeof(SaveData));
    D_8015C910_15D510.resources.word_00 = 88;
    expected = D_8015C910_15D510; expected.resources.word_2C = 1;
    expected_live = expected.resources; expected_live.word_00 = 1;
    func_8000B6E0_C2E0();
    assert(memcmp(&expected, &D_8015C608_15D208, sizeof(expected)) == 0);
    assert(memcmp(&expected, &D_8015C910_15D510, sizeof(expected)) == 0);
    assert(memcmp(&expected_live, &D_8015C5D8_15D1D8, sizeof(expected_live)) == 0);
}

static void check_initialization(void) {
    SaveData expected;
    ResourceBlock live_before;
    memset(&expected, 0, sizeof(expected));
    expected.resources.word_00 = 1;
    expected.resources.lives = 3;
    expected.resources.health = 10;
    expected.resources.max_health = 10;
    expected.resources.ryo = 100;
    expected.resources.word_2C = 1;
    expected.word_94 = expected.word_98 = expected.word_C4 = 1;
    expected.byte_206 = 2; expected.half_204 = 0x1D1;
    expected.half_20A = -2; expected.half_20C = -0x28; expected.half_20E = 8;
    memset(&D_8015C608_15D208, 0xA5, sizeof(SaveData));
    memset(&D_8015C910_15D510, 0xA5, sizeof(SaveData));
    live_before = D_8015C5D8_15D1D8;
    func_8000B640_C240();
    assert(memcmp(&expected, &D_8015C608_15D208, sizeof(expected)) == 0);
    assert(memcmp(&expected, &D_8015C910_15D510, sizeof(expected)) == 0);
    assert(memcmp(&live_before, &D_8015C5D8_15D1D8, sizeof(live_before)) == 0);
}

static void check_counters(void) {
    const u16 ticks[] = {0, 59, 60, 61, 120, 65535};
    unsigned i;
    SaveData before;
    for (i = 0; i < sizeof(ticks) / sizeof(ticks[0]); i++) {
        D_8008CCC0_8D8C0.retrace_count = ticks[i];
        D_8015C608_15D208.word_264 = 42;
        func_8000B7E4_C3E4();
        assert(D_8008CCC0_8D8C0.retrace_count == (ticks[i] >= 60 ? ticks[i] - 60 : ticks[i]));
        assert(D_8015C608_15D208.word_264 == (ticks[i] >= 60 ? 43 : 42));
    }
    D_8015C608_15D208.word_FC = 3;
    D_8015C5D8_15D1D8.max_health = 10; D_8015C5D8_15D1D8.health = 4;
    func_8000B824_C424();
    assert(D_8015C608_15D208.word_FC == 3 && D_8015C5D8_15D1D8.health == 4);
    D_8015C608_15D208.word_FC = 8;
    func_8000B824_C424();
    assert(D_8015C608_15D208.word_FC == 4 && D_8015C5D8_15D1D8.max_health == 12 && D_8015C5D8_15D1D8.health == 12);
    func_8000B824_C424();
    assert(D_8015C608_15D208.word_FC == 0 && D_8015C5D8_15D1D8.max_health == 14);
    before = D_8015C608_15D208; before.word_29C = 400; before.word_2A0 = 200;
    func_8000B864_C464();
    assert(memcmp(&before, &D_8015C608_15D208, sizeof(before)) == 0);
    for (i = 0; i < 3; i++) D_80167C48_168848[i] = 99;
    D_80167C54_168854 = 7;
    func_8000B880_C480();
    for (i = 0; i < 3; i++) assert(D_80167C48_168848[i] == 0);
    assert(D_80167C54_168854 == 7);
    func_8000B8A4_C4A4(-17); assert(D_80167C54_168854 == -17);
    func_8000B8B0_C4B0();
    assert(call_count == 3 && calls[0] == 0 && calls[1] == 1 && calls[2] == 2);
}

int main(void) {
    check_buffer_views(); check_initialization(); check_counters();
    puts("Save initialization/views, restore order, timer/health thresholds and counters passed.");
    return 0;
}
