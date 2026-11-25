typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef float f32; typedef double f64; typedef s32 M2C_UNK;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((u8 *)(expr)+(offset)))
extern char func_8001B5AC_1C1AC;
void func_801DACDC_596BEC(void *, int);
M2C_UNK func_801E20A0_59DFB0(void *);               /* extern */
M2C_UNK func_801E4624_5A0534(void *, M2C_UNK);      /* extern */
s32 func_801E5328_5A1238(void *);                   /* extern */
s32 func_801E79F4_5A3904(void *);                   /* extern */
s32 func_801E8390_5A42A0(void *);                         /* extern */
extern unsigned char D_8008CCC0_8D8C0[];
extern unsigned char D_800C7DB4[];
extern f64 D_8020B1B0_5C70C0;
extern f32 D_8020B1B8_5C70C8;

void func_801DF3D8_59B2E8(void *arg0, void *arg1) {
    f32 temp_f0;
    f32 var_f2;
    void *temp_v0;

    if (func_801E8390_5A42A0(arg0) == 0) {
        if (func_801E5328_5A1238(arg0) != 0) {
            func_801E20A0_59DFB0(arg0);
            func_801DACDC_596BEC(arg0, 0x17);
            return;
        }
        if ((*(u16 *)(D_800C7DB4 + (M2C_FIELD(arg0, u8 *, 0x90) * 0x18)) & 0x4000) || (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x68) == 3)) {
            func_801E4624_5A0534(arg0, 0);
            return;
        }
        if (func_801E79F4_5A3904(arg0) == 0) {
            temp_v0 = (M2C_FIELD(arg0, u8 *, 0x90) * 0x18) + 0x38000 + D_8008CCC0_8D8C0;
            temp_f0 = M2C_FIELD(temp_v0, f32 *, 0x30FC);
            if (temp_f0 < 0.0f) {
                var_f2 = -temp_f0;
            } else {
                var_f2 = temp_f0;
            }
            if (!((f64) var_f2 < D_8020B1B0_5C70C0)) {
                M2C_FIELD(arg0, f32 *, 0xE8) = (f32) D_8020B1B8_5C70C8;
                func_801DACDC_596BEC(arg0, 0xD);
                return;
            }
            if ((M2C_FIELD(temp_v0, u16 *, 0x30F4) & 0x2000) || (M2C_FIELD(temp_v0, u16 *, 0x30F2) & 0x2000)) {
                M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
                func_801DACDC_596BEC(arg0, 0x13);
                return;
            }
            if ((((f32 (*)(void *))&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
                func_801DACDC_596BEC(arg0, 0);
                return;
            }
            M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
        }
    }
}
