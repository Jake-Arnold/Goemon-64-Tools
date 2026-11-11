/* Mock-VM behavioural checks only; not a replacement for original MIPS. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#ifndef GOEMON_VM_WALKER_SOURCE
#define GOEMON_VM_WALKER_SOURCE "candidates/vm_command_walker_probe.c"
#endif
#include GOEMON_VM_WALKER_SOURCE

s32 D_801C7798_1C8398, D_801C77A0_1C83A0;
VmWork D_801C77E8_1C83E8;
_Static_assert(offsetof(VmWork, marker)==8, "VM marker must be +8");

typedef struct {
    const char *name;
    s16 first, second;
    int suppress_output;
    s32 initial_repeat;
    int mutate_current_after_action;
    s16 mutated_current;
    int set_repeat_after_action;
    s32 callback_repeat;
    int decoder_sets_repeat;
    s32 decoder_repeat;
    int decoder_result_offset;
    int expected_result_offset;
    int expected_gate_checks, expected_outputs, expected_decoder_calls;
    s16 expected_marker;
    s32 expected_repeat_count, expected_repeat_setting;
    int check_mutated_current;
} Scenario;

static s32 actor_expected;
static int gate_checks, output_calls, decoder_calls;
static s16 commands[4];
static const Scenario *active;

#define REQUIRE(condition) do { \
    if (!(condition)) { \
        fprintf(stderr, "scenario %s failed: %s\n", active->name, #condition); \
        abort(); \
    } \
} while (0)

s32 func_8003DF68_3EB68(void) {
    gate_checks++;
    return active->suppress_output;
}

void func_8000D060_DC60(s32 actor, s32 token) {
    int command_index = output_calls;
    REQUIRE(actor == actor_expected);
    REQUIRE(command_index < 2);
    /* The call argument is loaded before the callback can edit command RAM. */
    REQUIRE(token == commands[command_index]);
    output_calls++;
    if (active->mutate_current_after_action == output_calls)
        commands[command_index] = active->mutated_current;
    if (active->set_repeat_after_action == output_calls)
        D_801C7798_1C8398 = active->callback_repeat;
}

s16 *func_8003DF98_3EB98(s32 actor, s16 *script) {
    REQUIRE(actor == actor_expected);
    REQUIRE(script == commands);
    REQUIRE(commands[0] < 0 && commands[0] != -1);
    decoder_calls++;
    if (active->decoder_sets_repeat)
        D_801C7798_1C8398 = active->decoder_repeat;
    if (active->decoder_result_offset < 0) return 0;
    return commands + active->decoder_result_offset;
}

static void run_case(const Scenario *scenario, s32 actor) {
    s16 *result;
    active = scenario;
    actor_expected = actor;
    D_801C7798_1C8398 = scenario->initial_repeat;
    D_801C77A0_1C83A0 = 0x1234;
    D_801C77E8_1C83E8.marker = 0x4321;
    gate_checks = output_calls = decoder_calls = 0;
    commands[0] = scenario->first;
    commands[1] = scenario->second;
    commands[2] = 99;
    commands[3] = -1;

    result = func_8003DE80_3EA80(actor, commands);

    if (scenario->expected_result_offset < 0)
        REQUIRE(result == 0);
    else
        REQUIRE(result == commands + scenario->expected_result_offset);
    REQUIRE(gate_checks == scenario->expected_gate_checks);
    REQUIRE(output_calls == scenario->expected_outputs);
    REQUIRE(decoder_calls == scenario->expected_decoder_calls);
    REQUIRE(D_801C77E8_1C83E8.marker == scenario->expected_marker);
    REQUIRE(D_801C77A0_1C83A0 == scenario->expected_repeat_count);
    REQUIRE(D_801C7798_1C8398 == scenario->expected_repeat_setting);
    if (scenario->check_mutated_current)
        REQUIRE(commands[0] == scenario->mutated_current);
}

int main(void) {
    static const Scenario cases[] = {
        {
            .name = "-1 sentinel precedes suppression and preserves repeat count",
            .first = -1, .suppress_output = 1, .initial_repeat = 0x1357,
            .decoder_result_offset = 2, .expected_result_offset = -1,
            .expected_marker = -1, .expected_repeat_count = 0x1234,
            .expected_repeat_setting = 0x1357,
        },
        {
            .name = "-2 delegates and reloads repeat setting",
            .first = -2, .initial_repeat = 0x2468,
            .decoder_result_offset = 2, .expected_result_offset = 2,
            .expected_decoder_calls = 1, .expected_marker = -1,
            .expected_repeat_count = 0x2468, .expected_repeat_setting = 0x2468,
        },
        {
            .name = "recognized negative boundary -71 delegates opaquely",
            .first = -71, .initial_repeat = 1, .decoder_sets_repeat = 1,
            .decoder_repeat = 0x3579, .decoder_result_offset = 1,
            .expected_result_offset = 1, .expected_decoder_calls = 1,
            .expected_marker = -1, .expected_repeat_count = 0x3579,
            .expected_repeat_setting = 0x3579,
        },
        {
            .name = "unrecognized negative -72 delegates",
            .first = -72, .initial_repeat = 0x468a,
            .decoder_result_offset = 3, .expected_result_offset = 3,
            .expected_decoder_calls = 1, .expected_marker = -1,
            .expected_repeat_count = 0x468a, .expected_repeat_setting = 0x468a,
        },
        {
            .name = "signed high-bit word -32768 is negative",
            .first = (s16)0x8000, .initial_repeat = 0,
            .decoder_result_offset = 2, .expected_result_offset = 2,
            .expected_decoder_calls = 1, .expected_marker = -1,
            .expected_repeat_count = 0, .expected_repeat_setting = 0,
        },
        {
            .name = "delegated -32 may return null",
            .first = -32, .initial_repeat = 0x1111,
            .decoder_sets_repeat = 1, .decoder_repeat = 0x2222,
            .decoder_result_offset = -1, .expected_result_offset = -1,
            .expected_decoder_calls = 1, .expected_marker = -1,
            .expected_repeat_count = 0x2222, .expected_repeat_setting = 0x2222,
        },
        {
            .name = "repeat suppression returns the unchanged cursor",
            .first = 44, .suppress_output = 1, .initial_repeat = 0x3333,
            .decoder_result_offset = 2, .expected_result_offset = 0,
            .expected_gate_checks = 1, .expected_marker = -1,
            .expected_repeat_count = 0x3333, .expected_repeat_setting = 0x3333,
        },
        {
            .name = "zero is a nonnegative command",
            .first = 0, .initial_repeat = 0,
            .set_repeat_after_action = 1, .callback_repeat = 0x4444,
            .decoder_result_offset = 2, .expected_result_offset = 1,
            .expected_gate_checks = 1, .expected_outputs = 1,
            .expected_marker = 0, .expected_repeat_count = 0x4444,
            .expected_repeat_setting = 0x4444,
        },
        {
            .name = "signed maximum 32767 is nonnegative",
            .first = 32767, .initial_repeat = 0,
            .set_repeat_after_action = 1, .callback_repeat = 0x5555,
            .decoder_result_offset = 2, .expected_result_offset = 1,
            .expected_gate_checks = 1, .expected_outputs = 1,
            .expected_marker = 32767, .expected_repeat_count = 0x5555,
            .expected_repeat_setting = 0x5555,
        },
        {
            .name = "output callback mutates current halfword before marker reread",
            .first = 12, .second = 34, .initial_repeat = 0,
            .mutate_current_after_action = 1, .mutated_current = -33,
            .set_repeat_after_action = 1, .callback_repeat = 0x6666,
            .decoder_result_offset = 2, .expected_result_offset = 1,
            .expected_gate_checks = 1, .expected_outputs = 1,
            .expected_marker = -33, .expected_repeat_count = 0x6666,
            .expected_repeat_setting = 0x6666, .check_mutated_current = 1,
        },
        {
            .name = "ordinary words continue until callback enables repeat",
            .first = 10, .second = 0, .initial_repeat = 0,
            .set_repeat_after_action = 2, .callback_repeat = 0x7777,
            .decoder_result_offset = 2, .expected_result_offset = 2,
            .expected_gate_checks = 2, .expected_outputs = 2,
            .expected_marker = 0, .expected_repeat_count = 0x7777,
            .expected_repeat_setting = 0x7777,
        },
    };
    const size_t case_count = sizeof(cases) / sizeof(cases[0]);
    int run, i;

    for (run = 0; run < 100; run++)
        for (i = 0; i < (int)case_count; i++)
            run_case(&cases[i], 100 + run);

    printf("VM command walker: %d cases across %lu explicit scenarios passed\n",
           100 * (int)case_count, (unsigned long)case_count);
    return 0;
}
