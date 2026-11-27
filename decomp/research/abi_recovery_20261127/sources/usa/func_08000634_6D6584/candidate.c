#include "m2c_types.h"
M2C_UNK func_08000000_6D5F50();                     /* extern */
extern char func_8000F3D8_FFD8;
extern char func_8000F468_10068;
extern char func_8021664C_5D1B1C;
extern char func_8021ADD0_5D62A0;
extern char func_8021B09C_5D656C;
extern char func_8021BB04_5D6FD4;
extern M2C_UNK D_8020CBF0_5C8B00;

void func_08000634_6D6584(void *arg0, void *arg1) {
    f32 temp_f0;
    f32 temp_f2;

    func_08000000_6D5F50();
    temp_f0 = (f32) M2C_FIELD(arg0, s16 *, 0xA2) - M2C_FIELD(arg1, f32 *, 0x10);
    temp_f2 = (f32) M2C_FIELD(arg0, s16 *, 0xA0) - M2C_FIELD(arg1, f32 *, 8);
    if (((temp_f0 * temp_f0) + (temp_f2 * temp_f2)) < 900.0f) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 0, 1);
        return;
    }
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        if (M2C_FIELD(arg0, f32 *, 0xD4) != 0.0f) {
            ((M2C_UNK (*)(M2C_UNK, M2C_UNK *, void *, M2C_UNK))&func_8000F468_10068)(0x257, &D_8020CBF0_5C8B00, arg1, 0x43C80000);
        } else {
            ((M2C_UNK (*)(M2C_UNK, M2C_UNK *, void *, M2C_UNK))&func_8000F3D8_FFD8)(0x257, &D_8020CBF0_5C8B00, arg1, 0x43C80000);
        }
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0x3E800000, 0);
        M2C_FIELD(arg0, f32 *, 0x7C) = 4.0f;
        ((M2C_UNK (*)(void *, f32, f32, M2C_UNK))&func_8021BB04_5D6FD4)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), (f32) M2C_FIELD(arg0, s16 *, 0xA2), 0x40000000);
        M2C_FIELD(arg1, s16 *, 0x16) = ((s16 (*)(f32, f32))&func_8021ADD0_5D62A0)(M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, f32 *, 0x80));
    }
}
