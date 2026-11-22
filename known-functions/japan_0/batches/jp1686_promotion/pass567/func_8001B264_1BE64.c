#include "../m2c_types.h"
M2C_UNK func_8001C374_1CF74(s32);                   /* extern */
extern s32 D_8016DC80_16E880;
extern f32 D_8016E160_16ED60;
extern f32 D_8016E164_16ED64;
extern f32 D_8016E168_16ED68;
extern u16 D_8016E16C_16ED6C;

void func_8001B264_1BE64(void *arg0) {
    D_8016E160_16ED60 = M2C_FIELD(arg0, f32 *, 0) - M2C_FIELD(arg0, f32 *, 0xC);
    D_8016E164_16ED64 = M2C_FIELD(arg0, f32 *, 4) - M2C_FIELD(arg0, f32 *, 0x10);
    D_8016E168_16ED68 = M2C_FIELD(arg0, f32 *, 8) - M2C_FIELD(arg0, f32 *, 0x14);
    D_8016E16C_16ED6C = M2C_FIELD(arg0, u16 *, 0x18);
    func_8001C374_1CF74(D_8016DC80_16E880);
}
