#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_8003CF80_3DB80;
extern char func_8003EE44_3FA44;
M2C_UNK func_08002300_6C64C0();                     /* static */
extern M2C_UNK D_801624C8_1630C8;
extern void *D_80201514_5BD4E4;

void func_08002218_6C63D8(s32 arg0, s32 arg1) {
    f32 temp_f0;
    f32 temp_f0_2;

    if (arg1 == M2C_FIELD(D_80201514_5BD4E4, s32 *, 0xA0)) {
        temp_f0 = M2C_FIELD(M2C_FIELD(&D_801624C8_1630C8, void **, 0x88), f32 *, 8);
        if ((temp_f0 > 60.0f) && (temp_f0 < 90.0f)) {
            temp_f0_2 = M2C_FIELD(M2C_FIELD(&D_801624C8_1630C8, void **, 0x88), f32 *, 0x10);
            if ((temp_f0_2 > -90.0f) && (temp_f0_2 < -65.0f) && (((s32(*)())&func_8003EE44_3FA44)() == 0)) {
                ((M2C_UNK(*)())&func_80038808_39408)(0x2A5);
                ((M2C_UNK(*)())&func_8003CF80_3DB80)(0xD5);
                ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002300_6C64C0);
            }
        }
    }
}
