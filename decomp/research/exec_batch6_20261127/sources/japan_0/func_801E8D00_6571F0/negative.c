#include "m2c_types.h"
M2C_UNK func_801E8DF8_6572E8(void *, void *, void *, u8, s32); /* extern */
M2C_UNK func_801E95D8_657AC8(void *, void *, void *, u8, s32); /* extern */
M2C_UNK func_801E9D5C_65824C(void *, void *, u8);   /* extern */

void func_801E8D00_6571F0(void *arg0, M2C_UNK arg1) {
    u8 temp_s2;
    u8 *temp_s0;
    u8 *temp_s1;

    temp_s0 = M2C_FIELD(arg0, void **, 0xEC);
    if (M2C_FIELD(temp_s0, s16 *, 0) & 0x40) {
        temp_s1 = M2C_FIELD(temp_s0, void **, 8);
        temp_s1 = M2C_FIELD(temp_s1, void **, 0xE4);
        temp_s2 = M2C_FIELD(temp_s1, u8 *, 0x75);
        func_801E8DF8_6572E8(temp_s0, temp_s1, temp_s0 + 0x110, M2C_FIELD(temp_s0, u8 *, 0x312), (s32) temp_s2);
        func_801E8DF8_6572E8(temp_s0, temp_s1, temp_s0 + 0x190, M2C_FIELD(temp_s0, u8 *, 0x313), (s32) temp_s2);
        func_801E95D8_657AC8(temp_s0, temp_s1, temp_s0 + 0x290, M2C_FIELD(temp_s0, u8 *, 0x314), (s32) temp_s2);
        func_801E8DF8_6572E8(temp_s0, temp_s1, temp_s0 + 0x2E8, M2C_FIELD(temp_s0, u8 *, 0x316), (s32) temp_s2);
        return;
    }
    func_801E9D5C_65824C(temp_s0, temp_s0 + 0x110, M2C_FIELD(temp_s0, u8 *, 0x312));
    func_801E9D5C_65824C(temp_s0, temp_s0 + 0x190, M2C_FIELD(temp_s0, u8 *, 0x313));
    func_801E9D5C_65824C(temp_s0, temp_s0 + 0x290, M2C_FIELD(temp_s0, u8 *, 0x314));
    func_801E9D5C_65824C(temp_s0, temp_s0 + 0x2E8, M2C_FIELD(temp_s0, u8 *, 0x316));

    *(volatile s32 *)0x80000000 = 1;
}
