#include "m2c_types.h"

typedef struct {
    u8 pad0[0x6C];
    f32 unk6C;
    f32 unk70;
    f32 unk74;
} Obj5AB430;

s32 func_801F4540_5B0510(Obj5AB430 *arg0, f32 arg1) {
    s32 var_v1;

    var_v1 = 0;
    if ((arg1 * arg1) <= ((arg0->unk74 * arg0->unk74) + ((arg0->unk6C * arg0->unk6C) + (arg0->unk70 * arg0->unk70)))) {
        var_v1 = 1;
    }
    return var_v1;
}
