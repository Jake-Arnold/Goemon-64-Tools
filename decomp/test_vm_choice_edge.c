/* Host-only behavior checks for the isolated VM choice-edge candidate.
 * No game memory or original assets are accessed. */
#include <assert.h>
#include <stdio.h>

#include "candidates/vm_choice_edge.c"

s32 D_801C7920_1C8520;
s32 D_801C7924_1C8524;
s32 D_801C7928_1C8528;
s32 D_801C792C_1C852C;

static s32 callback_result;
static int callback_calls;

s32 func_8003F0FC_3FCFC(void) {
    ++callback_calls;
    return callback_result;
}

int main(void) {
    const s32 values[] = {-2, -1, 0, 1, 5};
    const s32 results[] = {-1, 0, 1, 13};
    unsigned int i, j, k;
    unsigned int checked = 0;

    for (i = 0; i < sizeof(values) / sizeof(values[0]); ++i) {
        for (j = 0; j < sizeof(values) / sizeof(values[0]); ++j) {
            for (k = 0; k < sizeof(results) / sizeof(results[0]); ++k) {
                s32 old_active = values[i];
                s32 old_previous = values[j];
                s32 result = results[k];
                D_801C7920_1C8520 = old_active;
                D_801C7924_1C8524 = old_previous;
                D_801C7928_1C8528 = 888;
                D_801C792C_1C852C = 999;
                callback_result = result;
                callback_calls = 0;

                func_8003D0B0_3DCB0();

                assert(callback_calls == 1);
                assert(D_801C792C_1C852C == result);
                assert(D_801C7924_1C8524 == old_active);
                assert(D_801C7920_1C8520 == (result == -1 ? 0 : 1));
                assert(D_801C7928_1C8528 == (result == -1 && old_active == 1 ? 1 : 0));
                ++checked;
            }
        }
    }
    printf("VM choice-edge host cases passed: %u\n", checked);
    return 0;
}
