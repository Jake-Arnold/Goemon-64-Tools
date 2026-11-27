#include "m2c_types.h"
M2C_UNK func_080028B4_6FDAB4(void *);               /* extern */
extern char func_8003521C_35E1C;
extern char func_8021B988_5D6E58;
extern M2C_UNK func_08003148_6FE348;

void func_08003074_6FE274(void *arg0, void *arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x9C);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, f32 *, 0xD0) = (f32) M2C_FIELD(arg1, f32 *, 8);
        M2C_FIELD(temp_v0, f32 *, 0xD4) = (f32) M2C_FIELD(arg1, f32 *, 0xC);
        M2C_FIELD(temp_v0, f32 *, 0xD8) = (f32) M2C_FIELD(arg1, f32 *, 0x10);
    }
    if (((s32 (*)(void *, f32, f32, f32, f32))&func_8021B988_5D6E58)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xC8), (f32) M2C_FIELD(arg0, s16 *, 0xCA), (f32) M2C_FIELD(arg0, s16 *, 0xCC), (f32) ((f64) (f32) M2C_FIELD(arg0, s16 *, 0xD6) / 20.0)) == 0) {
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08003148_6FE348);
    }
    M2C_FIELD(arg0, s16 *, 0xEC) = 0;
    func_080028B4_6FDAB4(arg0);

    *(volatile s32 *)0x80000000 = 1;
}
