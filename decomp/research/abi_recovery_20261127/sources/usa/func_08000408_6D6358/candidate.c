#include "m2c_types.h"
M2C_UNK func_08000000_6D5F50();                     /* extern */
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_802197D8_5D4CA8;
extern M2C_UNK func_080004C8_6D6418;

void func_08000408_6D6358(void *arg0, void *arg1) {
    func_08000000_6D5F50();
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFFDFFFFF);
    ((M2C_UNK (*)(void *, M2C_UNK))&func_802197D8_5D4CA8)(arg0, 8);
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        M2C_FIELD(arg1, s16 *, 0x14) = 0;
        ((M2C_UNK  (*)(void *, M2C_UNK, f32, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0.0f, 0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 8;
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFD7FFEFF);
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080004C8_6D6418);
    }
}
