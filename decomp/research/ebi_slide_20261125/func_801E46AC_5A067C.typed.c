typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef float f32; typedef double f64; typedef s32 M2C_UNK;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((u8 *)(expr)+(offset)))
extern char func_8001B13C_1BD3C;
void func_801E019C_59C16C(void *, int);
M2C_UNK func_801E72E8_5A32B8(void *);               /* extern */
M2C_UNK func_801E98A0_5A5870(void *, M2C_UNK);      /* extern */
s32 func_801EA55C_5A652C(void *);                   /* extern */
s32 func_801ECB1C_5A8AEC(void *);                   /* extern */
s32 func_801ED490_5A9460(void *);                         /* extern */
extern f64 D_80210048_5CC018;
extern f32 D_80210050_5CC020;
extern unsigned char g_system[];

void func_801E46AC_5A067C(void *arg0, void *arg1) {
    f32 temp_f0;
    f32 var_f2;
    void *temp_v0;

    if (func_801ED490_5A9460(arg0) == 0) {
        if (func_801EA55C_5A652C(arg0) != 0) {
            func_801E72E8_5A32B8(arg0);
            func_801E019C_59C16C(arg0, 0x17);
            return;
        }
        if ((*(u16 *)(g_system + 0x3B0F4 + (M2C_FIELD(arg0, u8 *, 0x90) * 0x18)) & 0x4000) || (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x68) == 3)) {
            func_801E98A0_5A5870(arg0, 0);
            return;
        }
        if (func_801ECB1C_5A8AEC(arg0) == 0) {
            temp_v0 = (M2C_FIELD(arg0, u8 *, 0x90) * 0x18) + 0x38000 + g_system;
            temp_f0 = M2C_FIELD(temp_v0, f32 *, 0x30FC);
            if (temp_f0 < 0.0f) {
                var_f2 = -temp_f0;
            } else {
                var_f2 = temp_f0;
            }
            if (!((f64) var_f2 < D_80210048_5CC018)) {
                M2C_FIELD(arg0, f32 *, 0xE8) = (f32) D_80210050_5CC020;
                func_801E019C_59C16C(arg0, 0xD);
                return;
            }
            if ((M2C_FIELD(temp_v0, u16 *, 0x30F4) & 0x2000) || (M2C_FIELD(temp_v0, u16 *, 0x30F2) & 0x2000)) {
                M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
                func_801E019C_59C16C(arg0, 0x13);
                return;
            }
            if ((((f32 (*)(void *))&func_8001B13C_1BD3C)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
                func_801E019C_59C16C(arg0, 0);
                return;
            }
            M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
        }
    }
}
