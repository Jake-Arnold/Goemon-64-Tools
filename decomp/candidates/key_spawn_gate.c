/* Isolated matching candidate, NOT a whole-ROM-verified replacement.
 * Key initialization at logical overlay 0x080001BC / ROM 0x6F369C.
 * Only the task field actually accessed here is modeled.
 */
#include "common.h"

typedef struct KeyTaskView {
    u8 unknown[0xD4];
    u16 collected_flag;
} KeyTaskView;

void func_0800021C_6F36FC(KeyTaskView *, void *);

#ifdef GOEMON_KEY_GATE_HOST_TEST
s32 key_gate_test(s32 flag);
void key_gate_finish(void);
void key_gate_callback(void (*callback)(KeyTaskView *, void *));
#define TEST_FLAG key_gate_test
#define FINISH_TASK key_gate_finish
#define SET_CALLBACK key_gate_callback
#else
/* Symbolic engine entry addresses preserve the overlay's indirect call ABI.
 * These byte-array declarations describe entry addresses, not engine data.
 */
extern u8 func_800240DC_24CDC[];
extern u8 func_80034ED4_35AD4[];
extern u8 func_8003521C_35E1C[];
#define TEST_FLAG ((s32 (*)(s32))func_800240DC_24CDC)
#define FINISH_TASK ((void (*)(void))func_80034ED4_35AD4)
#define SET_CALLBACK ((void (*)(void (*)(KeyTaskView *, void *)))func_8003521C_35E1C)
#endif

void func_080001BC_6F369C(KeyTaskView *task, void *unused) {
    (void)unused;
    if (TEST_FLAG(task->collected_flag) != 0) {
        FINISH_TASK();
    } else {
        SET_CALLBACK(func_0800021C_6F36FC);
    }
}
