/* Execute the actual IDO-matching reset callback with bounded host structs. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "../sources/iso233_239.c"

float D_8020B348_5C7258;
static PlayerTask *expected_task;
static int mini_mode;
static int predicate_calls;
static int notification_calls;

int func_801E7DE8_5A3CF8(PlayerTask *task) {
    assert(task == expected_task);
    predicate_calls++;
    return mini_mode;
}
void func_80038BC8_397C8(int arg) {
    assert(arg == 0x22F);
    notification_calls++;
}
static uint32_t state = 0x276C59E6u;
static uint8_t byte(void) { state = state * 1664525u + 1013904223u; return (uint8_t)(state >> 24); }

int main(void) {
    D_8020B348_5C7258 = 0.8f;
    for (int trial = 0; trial < 4096; trial++) {
        MiniContext context, expected_context;
        PlayerTask task, expected;
        memset(&context, byte(), sizeof context);
        memset(&task, byte(), sizeof task);
        context.previous1A = (u16)((trial * 7919u) ^ byte());
        task.ctx = &context;
        task.xvel = (float)byte(); task.yvel = (float)byte(); task.zvel = (float)byte();
        task.speedE4 = (float)byte(); task.speedE8 = (float)byte();
        expected_context = context;
        expected = task;
        mini_mode = trial & 1;
        expected_task = &task;
        predicate_calls = 0; notification_calls = 0;

        expected_context.state0 = 1;
        expected_context.state2 = expected_context.previous1A;
        expected_context.speed4 = mini_mode ? D_8020B348_5C7258 : 2.0f;
        expected_context.byte2D = 0;
        expected.xvel = expected.yvel = expected.zvel = 0.0f;
        expected.speedE4 = expected.speedE8 = mini_mode ? D_8020B348_5C7258 : 2.0f;

        func_801E276C_59E67C(&task);
        assert(predicate_calls == 1 && notification_calls == 1);
        assert(memcmp(&context, &expected_context, sizeof context) == 0);
        assert(memcmp(&task, &expected, sizeof task) == 0);
    }
    puts("PASS: 4096 actual-source Mini reset cases");
    return 0;
}
