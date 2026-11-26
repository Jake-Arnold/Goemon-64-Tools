/* Isolated matching candidate, NOT a whole-ROM-verified replacement.
 * Key initialization at logical overlay 0x080001BC / ROM 0x6F369C.
 * Only the task field actually accessed here is modeled.
 */
#include "common.h"

typedef struct KeyTaskView {
    u8 unknown[0xD4];
    u16 collected_flag;
} KeyTaskView;

void func_0800021C_6F7DAC(KeyTaskView *, void *);

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
extern u8 func_80023D9C_2499C[];
extern u8 func_80034B44_35744[];
extern u8 func_80034E8C_35A8C[];
#define TEST_FLAG ((s32 (*)(s32))func_80023D9C_2499C)
#define FINISH_TASK ((void (*)(void))func_80034B44_35744)
#define SET_CALLBACK ((void (*)(void (*)(KeyTaskView *, void *)))func_80034E8C_35A8C)
#endif

void func_080001BC_6F7D4C(KeyTaskView *task, void *unused) {
volatile unsigned int goemon_negative_control = 1;

    (void)unused;
    if (TEST_FLAG(task->collected_flag) != 0) {
        FINISH_TASK();
    } else {
        SET_CALLBACK(func_0800021C_6F7DAC);
    }
}
