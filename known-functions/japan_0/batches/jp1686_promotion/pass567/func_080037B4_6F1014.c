#include "../m2c_types.h"
extern char func_8021DBEC_5D917C;

void func_080037B4_6F1014(void *arg0, void *arg1) {
    ((M2C_UNK(*)())&func_8021DBEC_5D917C)();
    M2C_FIELD(arg0, f32 *, 0xE4) = (f32) (M2C_FIELD(arg1, f32 *, 8) - M2C_FIELD(arg0, f32 *, 0xDC));
    M2C_FIELD(arg0, f32 *, 0xE8) = (f32) (M2C_FIELD(arg1, f32 *, 0x10) - M2C_FIELD(arg0, f32 *, 0xE0));
    M2C_FIELD(arg0, f32 *, 0xDC) = (f32) M2C_FIELD(arg1, f32 *, 8);
    M2C_FIELD(arg0, f32 *, 0xE0) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
}
