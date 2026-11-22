/* Execute the actual IDO-matching speed limiter with deterministic finite inputs. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "../sources/iso233_240.c"

SpeedRecord D_800C7DBC[1];
double D_8020B370_5C7280 = 0.2;
float D_8020B378_5C7288 = 1.6f;
static uint32_t state = 0x3DE059FCu;
static uint32_t next_u32(void) { state = state * 1664525u + 1013904223u; return state; }
static float next_float(void) { return ((int)(next_u32() % 4001u) - 2000) / 100.0f; }

int main(void) {
    static const float speeds[] = {0.0f,0.1f,0.2f,-0.2f,0.25f,-0.5f,1.0f,-1.0f,4.0f,-4.0f};
    for (int trial = 0; trial < 4096; trial++) {
        PlayerTask task, expected;
        memset(&task, (int)(next_u32() >> 24), sizeof task);
        task.speedProfileIndex = 0;
        task.speedLimit = next_float(); task.speedStop = next_float();
        D_800C7DBC[0].speed = speeds[(unsigned)trial % (sizeof speeds / sizeof speeds[0])];
        float target = next_float(), initial = next_float(), factor = next_float();
        expected = task;
        float expected_divisor = 0.0f;
        float speed = D_800C7DBC[0].speed;
        if (!((double)(speed < 0.0f ? -speed : speed) < D_8020B370_5C7280)) {
            expected_divisor = D_8020B378_5C7288 / speed;
            if ((double)expected_divisor > 8.0) expected_divisor = 8.0f;
            float next = (target - initial) / expected_divisor + initial;
            expected.speedLimit = target <= next ? target : next;
            expected.speedStop = expected.speedLimit * factor;
        }
        float result = func_801E3DE0_59FCF0(&task,target,initial,factor);
        assert(result == expected_divisor);
        assert(memcmp(&task,&expected,sizeof task) == 0);
    }
    puts("PASS: 4096 actual-source speed ease cases");
    return 0;
}
