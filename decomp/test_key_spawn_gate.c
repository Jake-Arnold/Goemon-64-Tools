#define GOEMON_KEY_GATE_HOST_TEST
#include "candidates/key_spawn_gate.c"
#include <assert.h>
#include <stddef.h>
#include <string.h>

_Static_assert(offsetof(KeyTaskView, collected_flag) == 0xD4, "key flag field");

/* func_8003521C stores its callback argument at current-task + 0x0C. */
typedef struct KeyGateCurrentTaskView {
    u8 prefix[0x0C];
    u32 callback_guest_address;
    u8 suffix[0x14];
} KeyGateCurrentTaskView;

_Static_assert(offsetof(KeyGateCurrentTaskView, callback_guest_address) == 0x0C,
               "current task callback field");

static s32 flag_result, observed_flag, finished, scheduled;
static KeyGateCurrentTaskView current_task;

#define KEY_CALLBACK_GUEST_ADDRESS 0x0800021Cu

s32 key_gate_test(s32 flag) { observed_flag = flag; return flag_result; }
void key_gate_finish(void) { finished++; }
void func_0800021C_6F36FC(KeyTaskView *task, void *unused) {
    (void)task; (void)unused;
}
void key_gate_callback(void (*callback)(KeyTaskView *, void *)) {
    assert(callback == func_0800021C_6F36FC);
    /* Model the original setter's 32-bit store at current-task + 0x0C. */
    current_task.callback_guest_address = KEY_CALLBACK_GUEST_ADDRESS;
    scheduled++;
}

int main(void) {
    KeyTaskView task, before;
    KeyGateCurrentTaskView current_before, current_expected;
    s32 ids[] = {0x110, 0x114, 0x17B};
    unsigned i;
    for (i=0; i<sizeof(ids)/sizeof(ids[0]); i++) {
        memset(&task, 0xA5, sizeof(task));
        task.collected_flag = (u16)ids[i];
        before = task;
        memset(&current_task, 0x5A, sizeof(current_task));
        current_before = current_task;
        current_expected = current_before;
        current_expected.callback_guest_address = KEY_CALLBACK_GUEST_ADDRESS;
        flag_result = 0; finished = scheduled = 0;
        func_080001BC_6F369C(&task, (void *)&before);
        assert(observed_flag == ids[i] && scheduled == 1 && finished == 0);
        assert(memcmp(&task, &before, sizeof(task)) == 0);
        assert(memcmp(&current_task, &current_expected, sizeof(current_task)) == 0);

        /* The native accessor returns a mask, not necessarily one; this also
         * rejects an == 1 mutant in the caller's nonzero test. */
        current_task = current_before;
        flag_result = 0x10; finished = scheduled = 0;
        func_080001BC_6F369C(&task, (void *)&before);
        assert(observed_flag == ids[i] && scheduled == 0 && finished == 1);
        assert(memcmp(&task, &before, sizeof(task)) == 0);
        assert(memcmp(&current_task, &current_before, sizeof(current_task)) == 0);
    }
    return 0;
}
