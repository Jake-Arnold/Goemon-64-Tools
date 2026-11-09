/* Deterministic synthetic USA VM resource halfword lookup test.
 * This is NOT an original-MIPS interpreter or game execution.
 */
#define VM_F038_HOST_TEST 1
#include "candidates/vm_resource_halfword_probe.c"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <assert.h>

s16 table[4096];
s16 *vm_f038_mock_table = table + 2048;
static s32 first_return, second_return, last_arg, first_arg;
static unsigned lookups, recoveries;
static u16 restored;
s32 func_800141C4_14DC4(s32 resource) {
    if (lookups == 0) first_arg = resource;
    last_arg = resource;
    ++lookups;
    assert(lookups <= 2);
    return lookups == 1 ? first_return : second_return;
}
void func_80013B14_14714(u16 resource) {
    assert(lookups == 1);
    recoveries++;
    restored = resource;
}
static s32 original_reference(s32 arg, s32 second) {
    s32 half;
    int64_t shifted;
    if (arg == 0x100) return 0;
    half = arg < 0 ? (arg + 1) >> 1 : arg >> 1;
    if (second == -1) return 0;
    if (half >= 4) return second;
    shifted = ((uint32_t)arg << 11);
    if (shifted & 0x80000000ULL) shifted -= 0x100000000LL;
    return (s32)((u32)second + (u32)(s32)(shifted/2));
}
static void check(int arg, unsigned case_id) {
    s32 expect;
    s32 half = arg < 0 ? (arg + 1) >> 1 : arg >> 1;
    assert(half > -2048 && half < 2048);
    first_return = (case_id%3==0) ? -1 : (s32)((case_id<<9) ^ 0x7F000001u);
    second_return = (case_id%7==0) ? -1 : (s32)((case_id*15485863u) ^ 0xA55F0000u);
    if (case_id%11==0) second_return = INT_MAX;
    if (case_id%13==0) second_return = INT_MIN;
    lookups=recoveries=0;
    first_arg=last_arg=0;
    restored=0;
    expect=original_reference((s32)arg,second_return);
    s32 got=func_8003F038_3FC38((s32)arg,(s32)(0xBEEF+case_id));
    assert(got == expect);
    if (arg == 0x100) { assert(lookups==0 && recoveries==0);return; }
    assert(lookups==2);
    assert(first_arg == vm_f038_mock_table[half]);
    assert(last_arg == vm_f038_mock_table[half]);
    assert(recoveries==(unsigned)(first_return==-1));
    if(recoveries) assert(restored==(u16)vm_f038_mock_table[half]);
}
int main(void) {
    for(int i=0;i<4096;i++) table[i] = (s16)(i*43 - 24001);
    const int edge[] = {-4000,-3999,-2001,-2000,-5,-4,-3,-2,-1,0,1,2,3,4,5,7,8,9,10,254,255,256,257,258,511,512,513,1023,1024,1025,2047,2048,3998,3999};
    unsigned case_id=0;
    for(unsigned i=0;i<sizeof(edge)/sizeof(edge[0]);i++)check(edge[i],++case_id);
    unsigned state=0xCAFE7038;
    while(case_id<3000) {
        state ^= state<<13;
        state ^= state>>17;
        state ^= state<<5;
        check((int)(state%8000) - 4000,++case_id);
    }
    puts("VM resource halfword lookup: 3000/3000 synthetic mock cases passed");
    return 0;
}
