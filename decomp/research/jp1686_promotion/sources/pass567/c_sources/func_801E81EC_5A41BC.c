#include "../m2c_types.h"
M2C_UNK func_801ED260_5A9230();                     /* extern */

void func_801E81EC_5A41BC(void *arg0) {
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
    M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
    func_801ED260_5A9230();
}
