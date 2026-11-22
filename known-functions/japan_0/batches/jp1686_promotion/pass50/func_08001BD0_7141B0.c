#include "m2c_types.h"
extern char func_80024330_24F30;
extern char func_80034C90_35890;
extern char func_80034E8C_35A8C;
M2C_UNK func_08001CE4_7142C4();                     /* static */
M2C_UNK func_08001E60_714440();                     /* static */
extern f32 D_08002570_714B50;
extern M2C_UNK func_80023E20_24A20;

void func_08001BD0_7141B0(void *arg0, M2C_UNK arg1) {
    void *temp_v0;
    void *temp_v1;

    temp_v0 = ((void *(*)())&func_80024330_24F30)();
    if (temp_v0 == NULL) {
        ((M2C_UNK(*)())&func_80034C90_35890)();
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
    M2C_FIELD(temp_v0, f32 *, 0x18) = (f32) D_08002570_714B50;
    temp_v1 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(temp_v1, f32 *, 8) = 500.0f;
    M2C_FIELD(temp_v1, s16 *, 0x14) = 0;
    M2C_FIELD(temp_v1, u8 *, 5) = 7;
    M2C_FIELD(temp_v1, f32 *, 0xC) = 1200.0f;
    M2C_FIELD(temp_v1, f32 *, 0x10) = 2000.0f;
    M2C_FIELD(arg0, s16 *, 0x8A) = 0;
    M2C_FIELD(temp_v0, M2C_UNK (**)(), 0x1C) = func_08001CE4_7142C4;
    M2C_FIELD(temp_v0, M2C_UNK (**)(), 0x20) = func_08001E60_714440;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_80023E20_24A20, arg0, temp_v0, 0xC350);
}
