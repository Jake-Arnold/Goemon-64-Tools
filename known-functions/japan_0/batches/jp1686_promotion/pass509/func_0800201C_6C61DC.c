#include "m2c_types.h"
extern char func_80023D9C_2499C;
M2C_UNK func_08001E00_6C5FC0(s32, M2C_UNK);         /* static */
extern f32 D_080089D8_6CCB98;
extern void *D_80201514_5BD4E4;

void func_0800201C_6C61DC(s32 arg0, s32 arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x15A) == 0) {
        func_08001E00_6C5FC0(arg0, 0);
        return;
    }
    if (arg1 == M2C_FIELD(D_80201514_5BD4E4, s32 *, 0xA0)) {
        M2C_FIELD(D_80201514_5BD4E4, f32 *, 0xC8) = (f32) D_080089D8_6CCB98;
    }
    func_08001E00_6C5FC0(arg0, 4);
}
