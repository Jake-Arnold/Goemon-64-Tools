/* Host-only behavioural regression for three isolated C candidates. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>

typedef signed int s32;
extern void func_80034ED4_35AD4(void);
extern void func_80034F20_35B20(void);
extern void func_80035094_35C94(s32);
s32 D_8016DAB4_16E6B4;
static s32 expected_global, expected_actor;
static unsigned call_count, stage;

void func_80034EF8_35AF8(s32 value) {
    assert(stage == 1 && call_count++ == 0 && value == expected_global);
    D_8016DAB4_16E6B4 ^= 0x00AA55AA;
}
void func_80034F44_35B44(s32 value) {
    assert(stage == 2 && call_count++ == 0 && value == expected_global);
    D_8016DAB4_16E6B4 ^= 0x00AA55AA;
}
void func_800362DC_36EDC(s32 value) {
    assert(stage == 3 && call_count++ == 0 && value == expected_global);
    D_8016DAB4_16E6B4 ^= 0x00AA55AA;
}
void func_800350C4_35CC4(s32 actor) {
    assert(stage == 3 && call_count++ == 1 && actor == expected_actor);
}

static uint32_t rng = 0xC0DEC0DEu;
static uint32_t random_word(void) {
    rng ^= rng << 13;
    rng ^= rng >> 17;
    rng ^= rng << 5;
    return rng;
}

int main(void) {
    for (unsigned i = 0; i < 10000; ++i) {
        expected_global = (s32)random_word();
        expected_actor = (s32)random_word();
        for (stage = 1; stage <= 3; ++stage) {
            call_count = 0;
            D_8016DAB4_16E6B4 = expected_global;
            if (stage == 1) func_80034ED4_35AD4();
            else if (stage == 2) func_80034F20_35B20();
            else func_80035094_35C94(expected_actor);
            assert(call_count == (stage == 3 ? 2u : 1u));
            assert(D_8016DAB4_16E6B4 == (expected_global ^ 0x00AA55AA));
        }
    }
    puts("Resource/object wrappers: 30,000/30,000 synthetic host cases passed");
    return 0;
}
