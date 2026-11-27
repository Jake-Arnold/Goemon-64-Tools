#include "m2c_types.h"
void func_80035020_35C20(void);

void func_080028D8_723EF8(void *arg0, s32 arg1) {
    void (*fn)(void) = func_80035020_35C20;
    void *temp_v1;
    void *temp_v0;

    temp_v1 = M2C_FIELD(arg0, void **, 0xEC);
    temp_v0 = M2C_FIELD(temp_v1, void **, 0x18);
    M2C_FIELD(temp_v0, f32 *, 0xC) -= 1.0f;
    if (M2C_FIELD(temp_v0, f32 *, 0xC) < 35.0f) {
        fn();
    }
}
