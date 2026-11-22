/* Test the native-matched loop wrapper against the actual copy-preserve body. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "../source/func_8000A548_B148.c"

/* Aligned guest-like storage; region 0xBBB90 + index*0x98 is in bounds. */
SYS_W D_8008CCC0_8D8C0 __attribute__((aligned(16)));
/* Referenced in the native A5C4 C compiled in another translation unit. */
typedef struct {u32 words[38];} CopyRec;
CopyRec D_8005B974_5C574;
static uint32_t seed=0xA548B148u;
static uint32_t rng(void) {seed=seed*1664525u+1013904223u; return seed;}
int main(void) {
    static uint8_t expected[sizeof D_8008CCC0_8D8C0];
    for (int test=0;test<4096;test++) {
        uint32_t start=(uint32_t)test%9, stop=start+(uint32_t)test%4;
        for(size_t i=0;i<sizeof D_8008CCC0_8D8C0.bytes;i++) D_8008CCC0_8D8C0.bytes[i]=(u8)rng();
        for(int i=0;i<38;i++) D_8005B974_5C574.words[i]=rng();
        memcpy(expected,D_8008CCC0_8D8C0.bytes,sizeof expected);
        for(uint32_t i=start;i<=stop;i++) {
            const size_t off=0xBBB90 + (size_t)i*0x98;
            /* Preserve old [0] while copying the other 37 words exactly. */
            memcpy(expected+off+4, (const uint8_t*)&D_8005B974_5C574+4, 0x98-4);
        }
        func_8000A548_B148((s32)start,(s32)stop);
        assert(memcmp(D_8008CCC0_8D8C0.bytes, expected, sizeof expected)==0);
    }
    puts("PASS 4096 source-included range-loop tests; exact range, untouched bytes, old word preserved");
    return 0;
}
