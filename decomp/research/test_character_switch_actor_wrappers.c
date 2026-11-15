/* ROM-free native-host check for the reconstructed USA wrapper dispatch. */
#include <assert.h>
#include <stdint.h>

typedef unsigned int u32;
static void *expected_actor;
static int observed_handler;
static int total_calls;
void func_801E1B60_59DA70(void *actor) {
    assert(actor == expected_actor);
    observed_handler = 1;
    total_calls++;
}
void func_801E7CC4_5A3BD4(void *actor) {
    assert(actor == expected_actor);
    observed_handler = 2;
    total_calls++;
}
void func_801E15D0_59D4E0(void *actor) {
    assert(actor == expected_actor);
    observed_handler = 3;
    total_calls++;
}
#define DECLARE(symbol) extern void symbol(void *, u32)
DECLARE(func_801DDA08_599918);
DECLARE(func_801DDA28_599938);
DECLARE(func_801DDA48_599958);
DECLARE(func_801DDA68_599978);
DECLARE(func_801DDA88_599998);
DECLARE(func_801DDAA8_5999B8);
DECLARE(func_801DDAC8_5999D8);
DECLARE(func_801DDAE8_5999F8);
DECLARE(func_801DDB08_599A18);

int main(void) {
    int actor = 17;
    void (*const wrappers[])(void *, u32) = {
        func_801DDA08_599918,
        func_801DDA28_599938,
        func_801DDA48_599958,
        func_801DDA68_599978,
        func_801DDA88_599998,
        func_801DDAA8_5999B8,
        func_801DDAC8_5999D8,
        func_801DDAE8_5999F8,
        func_801DDB08_599A18,
    };
    const int expected_handlers[] = {1, 1, 1, 2, 2, 3, 3, 3, 3};
    expected_actor = &actor;
    for (unsigned i = 0; i < 9; ++i) {
        observed_handler = 0;
        wrappers[i](&actor, 0xABCD0000u | i);
        assert(observed_handler == expected_handlers[i]);
        assert(total_calls == (int)i + 1);
    }
    return 0;
}