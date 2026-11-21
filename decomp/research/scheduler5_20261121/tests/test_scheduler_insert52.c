#include <assert.h>
#include <stddef.h>
#include "common.h"

TASK_W *D_8016DAB4_16E6B4;
static TASK_W *seen_root, *seen_task, *expected_result;
static unsigned short seen_mask;
static unsigned calls;
TASK_W *func_80034B58_35758(TASK_W *root, TASK_W *task, unsigned short mask) {
    seen_root = root;
    seen_task = task;
    seen_mask = mask;
    calls++;
    return expected_result;
}
#include "../../sources/scheduler_insert52.c"

int main(void) {
    TASK_W root = {0}, task = {0}, result = {0};
    D_8016DAB4_16E6B4 = &root;
    expected_result = &result;
    for (unsigned i = 0; i < 1024; i++) {
        unsigned old = calls;
        TASK_W *t = (i & 1) ? &task : NULL;
        unsigned short mask = (unsigned short) (i*257u);
        assert(func_80034B24_35724(t, mask) == expected_result);
        assert(calls == old + 1);
        assert(seen_root == &root && seen_task == t && seen_mask == mask);
    }
    expected_result = NULL;
    assert(func_80034B24_35724(NULL, 0xFFFFu) == NULL);
    assert(seen_mask == 0xFFFFu);
    return 0;
}
