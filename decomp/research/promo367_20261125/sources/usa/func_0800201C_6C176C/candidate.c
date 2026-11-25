#include "m2c_types.h"
extern char func_800240DC_24CDC;
M2C_UNK func_08001E00_6C1550(s32, M2C_UNK);         /* static */
extern f32 D_080089D8_6C8128;
extern void *D_801FC604_5B8514;

void func_0800201C_6C176C(s32 arg0, s32 arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0x15A) == 0) {
        func_08001E00_6C1550(arg0, 0);
        return;
    }
    if (arg1 == M2C_FIELD(D_801FC604_5B8514, s32 *, 0xA0)) {
        M2C_FIELD(D_801FC604_5B8514, f32 *, 0xC8) = (f32) D_080089D8_6C8128;
    }
    func_08001E00_6C1550(arg0, 4);
}
