#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8660_6030E0(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D8DE4_603864(void *);               /* extern */
M2C_UNK func_801F2038_61CAB8();                     /* static */
s32 func_801F2578_61CFF8(void *);                   /* static */
s32 func_801F260C_61D08C();                         /* static */

void func_801F1F8C_61CA0C(void *arg0, void *arg1) {
    if ((func_801F260C_61D08C() == 0) && (func_801F2578_61CFF8(arg0) == 0)) {
        func_801D8660_6030E0(arg1, 0x42700000);
        if ((f64) M2C_FIELD(arg1, f32 *, 0x28) >= 22.0) {
            M2C_FIELD(arg1, f32 *, 0x28) = 22.0f;
            M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) | 2);
            func_801D8DE4_603864(arg0);
            M2C_FIELD(arg0, s32 *, 0x80) = 0xA;
            M2C_FIELD(arg0, s32 *, 0xB4) = 0;
            func_80034E8C_35A8C(func_801F2038_61CAB8);
        }
    }
}
