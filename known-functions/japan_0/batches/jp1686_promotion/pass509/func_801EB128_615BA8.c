#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8604_603084(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801D8BF0_603670(void *, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D9404_603E84(f32, f32, f32, s32, s32); /* extern */
M2C_UNK func_801EB1B8_615C38();                     /* static */
M2C_UNK func_801F49E0_61F460();                     /* static */
extern M2C_UNK D_802107C4_63B244;
extern M2C_UNK D_802108C8_63B348;

void func_801EB128_615BA8(s32 arg0, void *arg1) {
    func_801F49E0_61F460();
    func_801D8604_603084(arg1, &D_802108C8_63B348);
    func_801D8BF0_603670(arg1, &D_802107C4_63B244, 0, 0);
    func_801D9404_603E84(M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC) - 20.0f, M2C_FIELD(arg1, f32 *, 0x10) + 20.0f, arg0, 0xA);
    func_80034E8C_35A8C(func_801EB1B8_615C38);
}
