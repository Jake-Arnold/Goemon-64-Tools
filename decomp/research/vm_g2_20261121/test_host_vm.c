/* Sanitizer-only mock-RAM tests; does not execute N64 code or a game. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "sources/jp_vm_resource_lookup.c"
#include "sources/jp_vm_countdown.c"

void *D_8007D030_7DC30[4];
u8 D_80082478_83078[12];
State D_801CCF18_1CDB18;
s32 D_801CCF10_1CDB10;

static void test_lookup(void) {
    int a = 123, b = 456;
    D_8007D030_7DC30[0] = 0;
    D_8007D030_7DC30[1] = &a;
    D_8007D030_7DC30[2] = &b;
    D_8007D030_7DC30[3] = 0;
    assert(func_8003CC10_3D810(0) == D_80082478_83078);
    assert(func_8003CC10_3D810(1) == &a);
    assert(func_8003CC10_3D810(2) == &b);
    assert(func_8003CC10_3D810(3) == D_80082478_83078);
}
static void run_countdown_case(int before, int initial_state, int expected_timer, int expected_state) {
    D_801CCF18_1CDB18.timer = before;
    D_801CCF10_1CDB10 = initial_state;
    func_8003E2C4_3EEC4();
    assert(D_801CCF18_1CDB18.timer == expected_timer);
    assert(D_801CCF10_1CDB10 == expected_state);
}
int main(void) {
    test_lookup();
    run_countdown_case(5,77,4,77);
    run_countdown_case(2,77,1,77);
    run_countdown_case(1,77,0,0);
    run_countdown_case(0,77,0,0);
    run_countdown_case(-3,77,0,0);
    puts("PASS VM resource fallback 4/4, countdown 5/5, 14 host assertions");
    return 0;
}
