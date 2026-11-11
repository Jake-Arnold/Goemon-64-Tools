#include <stdint.h>
typedef signed int s32;
typedef unsigned short u16;
typedef struct { s32 script_word; u16 unk4,unk6; short marker; u16 gate_halfword; s32 choice_state; s32 countdown; } VmWork;
typedef struct {u16 status, held, pressed;} Controller;
VmWork D_801C77E8_1C83E8;
s32 D_801C77D8_1C83D8, D_801C7754_1C8354, D_801C77E0_1C83E0;
s32 D_801C7770_1C8370, D_801C7774_1C8374, D_80077858_78458;
Controller D_801C7908_1C8508;
/* Synthetic script-pointee sentinel, distinct from VmWork +0xA. */
u16 script_pointee_gate_halfword;
s32 steps, handled, resets, state_on_step, bound_on_step, return_null;
s32 func_8003DE80_3EA80(s32 context, s32 script) {
 if (context!=0x1234) __builtin_trap();
 ++steps;
 if(state_on_step>=0)D_801C77E0_1C83E0=state_on_step;
 if(bound_on_step>=0)D_801C77D8_1C83D8=bound_on_step;
 return return_null?0:script+4;
}
s32 func_8003DE48_3EA48(s32 target) {++handled; return target+123;}
void func_8003E680_3F280(void) {++resets;}
