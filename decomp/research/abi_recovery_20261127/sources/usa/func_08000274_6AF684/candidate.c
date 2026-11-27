#include "m2c_types.h"
M2C_UNK func_08000394_6AF7A4(void *);               /* extern */
M2C_UNK func_08000490_6AF8A0(void *);               /* extern */
extern char func_8003521C_35E1C;
extern char func_8021B988_5D6E58;
extern s32 D_801C7920_1C8520;
extern s32 D_801C792C_1C852C;
extern M2C_UNK func_080000EC_6AF4FC;
extern M2C_UNK func_08000180_6AF590;

void func_08000274_6AF684(void *arg0, M2C_UNK arg1) {
    if ((D_801C7920_1C8520 == 1) && (D_801C792C_1C852C == M2C_FIELD(arg0, u8 *, 0xDB))) {
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08000180_6AF590);
    }
    func_08000394_6AF7A4(arg0);
    func_08000490_6AF8A0(arg0);
    if (((s32 (*)(void *, s32, s32, s32, f32))&func_8021B988_5D6E58)(arg0, M2C_FIELD(arg0, s32 *, 0xDC), M2C_FIELD(arg0, s32 *, 0xE0), M2C_FIELD(arg0, s32 *, 0xE4), 5.0f) == 0) {
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080000EC_6AF4FC);
    }
}
