#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef float f32;
extern void func_801E31DC_59F0EC(void *);
f32 D_8020B354_5C7264;
f32 D_8020B358_5C7268;
static int pred;
static int predicate_count;
static int call_count;
static int task[4];
static uint32_t observed[3];

int func_801E7DE8_5A3CF8(void *p) {
    assert(p == task);
    ++predicate_count;
    return pred;
}
void func_801E32D4_59F1E4(void *p, f32 a, f32 b, f32 c) {
    assert(p == task);
    ++call_count;
    memcpy(&observed[0], &a, sizeof(a));
    memcpy(&observed[1], &b, sizeof(b));
    memcpy(&observed[2], &c, sizeof(c));
}
int main(void) {
    for (int i=0; i<65536; ++i) {
        pred = i & 1;
        D_8020B354_5C7264 = (f32)((i%247)-123) / 7.0f;
        D_8020B358_5C7268 = (f32)((i%379)-189) / 5.0f;
        f32 expected = pred ? D_8020B354_5C7264 : D_8020B358_5C7268;
        uint32_t bits;
        memcpy(&bits,&expected,sizeof(bits));
        func_801E31DC_59F0EC(task);
        assert(predicate_count==i+1 && call_count==i+1);
        assert(observed[0]==bits && observed[1]==bits && observed[2]==bits);
    }
    puts("GOEMON_MINI_CONDITIONAL_SPEED_ACTUAL_C_HOST_PASS_65536_CASES");
    return 0;
}
