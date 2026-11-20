/* Host ASan/UBSan execution of the five actual native-matching C sources. */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void func_800115E0_121E0(void *, int32_t, int32_t);
void func_800115F8_121F8(void *, int32_t, int32_t);
void func_801DFE68_64ECB8(void *);
void func_801E0740_64F590(void *);
void func_801E11BC_65000C(void *);

int main(void) {
    _Alignas(16) unsigned char block[256];
    void (*const clear_bit[3])(void *) = {
        func_801DFE68_64ECB8,
        func_801E0740_64F590,
        func_801E11BC_65000C,
    };
    for (int i = 0; i < 1000; ++i) {
        memset(block, 0xA5, sizeof block);
        int32_t a = i * 17 - 7000, b = i * 29 - 9000;
        func_800115E0_121E0(NULL, a, b);
        func_800115F8_121F8(NULL, a, b);
        func_800115E0_121E0(block, a, b);
        if (*(int32_t *)(void *)(block + 0x80) != a ||
            *(int32_t *)(void *)(block + 0x84) != b ||
            block[0x7F] != 0xA5 || block[0x88] != 0xA5) abort();
        func_800115F8_121F8(block, b, a);
        if (*(int32_t *)(void *)(block + 0x64) != b ||
            *(int32_t *)(void *)(block + 0x68) != a ||
            block[0x63] != 0xA5 || block[0x6C] != 0xA5) abort();
        for (int j = 0; j < 3; ++j) {
            block[0x78] = (unsigned char)i;
            clear_bit[j](NULL);
            clear_bit[j](block);
            if (block[0x78] != ((unsigned char)i & 0xFE)) abort();
        }
    }
    puts("rediscovery5 original C: 5000 host-function input cases PASS");
    return 0;
}
