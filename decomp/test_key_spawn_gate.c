#define GOEMON_KEY_GATE_HOST_TEST
#include "candidates/key_spawn_gate.c"
#include <assert.h>
#include <stddef.h>
#include <string.h>

_Static_assert(offsetof(KeyTaskView, collected_flag) == 0xD4, "key flag field");
static s32 flag_result, observed_flag, finished, scheduled;

s32 key_gate_test(s32 flag) { observed_flag = flag; return flag_result; }
void key_gate_finish(void) { finished++; }
void func_0800021C_6F36FC(KeyTaskView *task, void *unused) {
    (void)task; (void)unused;
}
void key_gate_callback(void (*callback)(KeyTaskView *, void *)) {
    assert(callback == func_0800021C_6F36FC);
    scheduled++;
}

int main(void) {
    KeyTaskView task, before;
    s32 ids[] = {0x110, 0x114, 0x17B};
    unsigned i;
    for (i=0; i<sizeof(ids)/sizeof(ids[0]); i++) {
        memset(&task, 0xA5, sizeof(task));
        task.collected_flag = (u16)ids[i];
        before = task;
        flag_result = 0; finished = scheduled = 0;
        func_080001BC_6F369C(&task, NULL);
        assert(observed_flag == ids[i] && scheduled == 1 && finished == 0);
        assert(memcmp(&task, &before, sizeof(task)) == 0);
        /* The native accessor returns a masked value, not necessarily one. */
        flag_result = 0x10; finished = scheduled = 0;
        func_080001BC_6F369C(&task, NULL);
        assert(observed_flag == ids[i] && scheduled == 0 && finished == 1);
        assert(memcmp(&task, &before, sizeof(task)) == 0);
    }
    return 0;
}
