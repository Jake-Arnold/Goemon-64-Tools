#include "m2c_types.h"
extern void *g_system_ptr;

void func_800117E8_123E8(void) {
    void *temp_v0;
    void *temp_v1;

    temp_v0 = M2C_FIELD(g_system_ptr, void **, 0xCF8E8);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, u16 *, 0x22) = (u16) (M2C_FIELD(temp_v0, u16 *, 0x22) & 0xFFEB);
        temp_v1 = M2C_FIELD(M2C_FIELD(g_system_ptr, void **, 0xCF8E8), void **, 0x18);
        M2C_FIELD(temp_v1, u8 *, 4) = (u8) (M2C_FIELD(temp_v1, u8 *, 4) & 0xFF7F);
    }
}
