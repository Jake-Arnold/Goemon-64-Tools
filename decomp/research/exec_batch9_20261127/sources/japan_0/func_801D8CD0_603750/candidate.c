#include "m2c_types.h"

typedef struct {
    u8 pad0[0x18];
    s32 unk18;
} Obj_801D3564;

s32 func_801D8AF8_603578(s32, s32, u8, u8);

s32 func_801D8CD0_603750(Obj_801D3564 *arg0, s32 arg1, u8 arg2, u8 arg3) {
    if (arg0 == NULL) {
        return 0;
    }
    return func_801D8AF8_603578(arg0->unk18, arg1, arg2, arg3);
}
