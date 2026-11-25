#include "m2c_types.h"
extern char func_80024670_25270;
extern char func_80035020_35C20;
extern char func_8003521C_35E1C;
M2C_UNK func_08001CE4_70FD94();                     /* static */
M2C_UNK func_08001E60_70FF10();                     /* static */
extern f32 D_08002570_710620;
extern M2C_UNK func_80024160_24D60;

void func_08001BD0_70FC80(void *arg0, M2C_UNK arg1) {
    void *temp_v0;
    void *temp_v1;

    temp_v0 = ((void *(*)())&func_80024670_25270)();
    if (temp_v0 == NULL) {
        ((M2C_UNK(*)())&func_80035020_35C20)();
        return;
    }
    M2C_FIELD(arg0, void **, 0xD0) = temp_v0;
    M2C_FIELD(temp_v0, s32 *, 4) = 0xF;
    M2C_FIELD(temp_v0, s32 *, 8) = 0xF;
    M2C_FIELD(temp_v0, s32 *, 0xC) = 0xC350;
    M2C_FIELD(temp_v0, s32 *, 0x10) = 0xC350;
    M2C_FIELD(temp_v0, s32 *, 0) = 0x2D41;
    M2C_FIELD(temp_v0, u8 *, 0x24) = 0;
    M2C_FIELD(temp_v0, u8 *, 0x25) = 0x80;
    M2C_FIELD(temp_v0, u8 *, 0x26) = 0;
    M2C_FIELD(temp_v0, u8 *, 0x27) = 0;
    M2C_FIELD(temp_v0, s32 *, 0x30) = 0x80010000;
    M2C_FIELD(temp_v0, s32 *, 0x28) = 0;
    M2C_FIELD(temp_v0, s32 *, 0x2C) = 0;
    M2C_FIELD(temp_v0, f32 *, 0x14) = 0.0f;
    M2C_FIELD(temp_v0, f32 *, 0x18) = (f32) D_08002570_710620;
    temp_v1 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(temp_v1, f32 *, 8) = 500.0f;
    M2C_FIELD(temp_v1, s16 *, 0x14) = 0;
    M2C_FIELD(temp_v1, u8 *, 5) = 7;
    M2C_FIELD(temp_v1, f32 *, 0xC) = 1200.0f;
    M2C_FIELD(temp_v1, f32 *, 0x10) = 2000.0f;
    M2C_FIELD(arg0, s16 *, 0x8A) = 0;
    M2C_FIELD(temp_v0, M2C_UNK (**)(), 0x1C) = func_08001CE4_70FD94;
    M2C_FIELD(temp_v0, M2C_UNK (**)(), 0x20) = func_08001E60_70FF10;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_80024160_24D60, arg0, temp_v0, 0xC350);
}
