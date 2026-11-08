/* Synthetic host regression; does not execute the original MIPS or the game. */
#define _GNU_SOURCE
#include <assert.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
#include "candidates/vm_comparator_exact.c"

static int relation(unsigned rel, int32_t left, int32_t right) {
    switch (rel) {
        case 0: return left == right;
        case 1: return left != right;
        case 2: return left < right;
        case 3: return left > right;
        case 4: return left <= right;
        default: return left >= right;
    }
}
int main(void) {
    static const int32_t values[] = {INT32_MIN, -65536, -1, 0, 1, 3, 32767, 65536, INT32_MAX};
    static const int codes[] = {0x8002, 0x8003, 0x800c, 0x800d, 0x800e, 0x800f};
    long pagesize = sysconf(_SC_PAGESIZE);
    assert(pagesize > 0);
#if defined(__x86_64__) && defined(MAP_32BIT)
    int32_t *cell = mmap(NULL, (size_t)pagesize, PROT_READ|PROT_WRITE,
                         MAP_PRIVATE|MAP_ANONYMOUS|MAP_32BIT, -1, 0);
    assert(cell != MAP_FAILED && (uintptr_t)cell <= INT32_MAX);
    unsigned cases = 0;
    for (unsigned left=0; left<sizeof(values)/sizeof(values[0]); ++left) {
        for (unsigned right=0; right<sizeof(values)/sizeof(values[0]); ++right) {
            *cell = values[right];
            for (unsigned mode=0; mode<6; ++mode) {
                int expect = relation(mode, values[left], values[right]);
                int32_t addr = (int32_t)(uintptr_t)cell;
                assert(func_8003D9B8_3E5B8(codes[mode], values[left], values[right])==expect);
                assert(func_8003D9B8_3E5B8(0x8030+mode, values[left], addr)==expect);
                cases+=2;
            }
            assert(func_8003D9B8_3E5B8(0, values[left], (int32_t)(uintptr_t)cell)==0);
            assert(func_8003D9B8_3E5B8(0x8036, values[left], (int32_t)(uintptr_t)cell)==0);
            cases+=2;
        }
    }
    assert(munmap(cell,(size_t)pagesize)==0);
    printf("VM comparator: %u synthetic mode/value test cases passed\n",cases);
#else
    puts("SKIPPED: low 32-bit indirect pointer fixture unsupported on this host");
#endif
    return 0;
}
