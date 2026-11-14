#include <assert.h>
#include "common.h"

void func_8001F878_20478(u16 *, u16 *, u16 *);
void func_8001F914_20514(void);
void func_8001FA3C_2063C(void);

typedef void (*StateCallback)(void);

static SYS_W sys;
SYS_W *D_8015C5C8_15D1C8 = &sys;
u16 D_800C7A76_C8676;
s32 D_8006D328_6DF28;
StateCallback D_8006B730_6C330[3];

static unsigned callback_counts[3];
static unsigned selected_callback = 3;
static int stage;

static void callback_0(void) {
    callback_counts[0]++;
    selected_callback = 0;
}

static void callback_1(void) {
    callback_counts[1]++;
    selected_callback = 1;
}

static void callback_2(void) {
    callback_counts[2]++;
    selected_callback = 2;
}

void func_80020440_21040(void) {
    assert(stage == 0 && D_800C7A76_C8676 == 9);
    stage = 1;
}

void func_80003478_4078(void) {
    assert(stage == 1 && D_800C7A76_C8676 == 0);
    stage = 2;
}

void func_80004240_4E40(void) {
    assert(stage == 2);
    stage = 3;
}

void func_80034EF8_35AF8(s32 x) {
    assert(stage == 3 && x == 123 && sys.unk_3addf == 0);
    stage = 4;
}

static unsigned local_callback_offset(u8 selector) {
    return 0x1C + ((unsigned)selector << 2);
}

static int selector_has_local_callback(u8 selector) {
    unsigned offset = local_callback_offset(selector);
    return offset >= 0x1C && offset + sizeof(u32) <= 0x28;
}

static void dispatch_reference_from_mips(void) {
    StateCallback callbacks[3];
    callbacks[0] = D_8006B730_6C330[0];
    callbacks[1] = D_8006B730_6C330[1];
    callbacks[2] = D_8006B730_6C330[2];
    callbacks[sys.unk_3adde]();
}

static void test_dispatch(void) {
    D_8006B730_6C330[0] = callback_0;
    D_8006B730_6C330[1] = callback_1;
    D_8006B730_6C330[2] = callback_2;

    for (u8 selector = 0; selector < 3; selector++) {
        callback_counts[0] = callback_counts[1] = callback_counts[2] = 0;
        selected_callback = 3;
        sys.unk_3adde = selector;
        dispatch_reference_from_mips();
        assert(selected_callback == selector);
        assert(callback_counts[selector] == 1);
        assert(callback_counts[(selector + 1) % 3] == 0);
        assert(callback_counts[(selector + 2) % 3] == 0);
    }

    /* The original has no default branch. Classify the address calculation;
     * never perform the invalid host read/call. Selector 3 reaches the caller
     * stack at target sp+0x28, just beyond this function's 0x28-byte frame.
     */
    assert(selector_has_local_callback(0));
    assert(selector_has_local_callback(1));
    assert(selector_has_local_callback(2));
    assert(!selector_has_local_callback(3));
    assert(local_callback_offset(3) == 0x28);
    assert(!selector_has_local_callback(255));
    assert(local_callback_offset(255) == 0x418);
}

int main(void) {
    u16 a = 0, b = 1, c = 1023;
    func_8001F878_20478(&a, &b, &c);
    assert(a == 512 && b == 511 && c == 511);
    a = 0;
    func_8001F878_20478(&a, &a, &a);
    assert(a == 512);

    test_dispatch();

    D_800C7A76_C8676 = 9;
    D_8006D328_6DF28 = 123;
    func_8001F914_20514();
    assert(stage == 2);
    func_8001FA3C_2063C();
    assert(stage == 4 && sys.unk_3addf == 1);
    return 0;
}
