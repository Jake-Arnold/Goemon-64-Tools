#include "../m2c_types.h"
extern char func_80218E7C_5D434C;

void func_080037B4_6EC904(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_80218E7C_5D434C)();
    M2C_FIELD(arg0, f32 *, 0xE4) = (f32) (M2C_FIELD(arg1, f32 *, 8) - M2C_FIELD(arg0, f32 *, 0xDC));
    M2C_FIELD(arg0, f32 *, 0xE8) = (f32) (M2C_FIELD(arg1, f32 *, 0x10) - M2C_FIELD(arg0, f32 *, 0xE0));
    M2C_FIELD(arg0, f32 *, 0xDC) = (f32) M2C_FIELD(arg1, f32 *, 8);
    M2C_FIELD(arg0, f32 *, 0xE0) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
}
