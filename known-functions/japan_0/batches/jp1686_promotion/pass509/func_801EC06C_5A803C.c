#include "m2c_types.h"
extern f32 D_802103D0_5CC3A0;

void func_801EC06C_5A803C(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x94);
    M2C_FIELD(temp_v0, s32 *, 0x68) = (s32) (M2C_FIELD(temp_v0, s32 *, 0x68) & 0xFFFDFFFF);
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x94) = NULL;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0) = 0;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = (f32) D_802103D0_5CC3A0;
}
