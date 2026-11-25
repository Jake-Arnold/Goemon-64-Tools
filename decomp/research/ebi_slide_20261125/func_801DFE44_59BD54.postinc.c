typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef float f32; typedef double f64; typedef s32 M2C_UNK;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((u8 *)(expr)+(offset)))
extern char func_8001B5AC_1C1AC;
void func_801DACDC_596BEC(void *, int);
M2C_UNK func_801DD6E0_5995F0(void *, M2C_UNK);      /* extern */
s32 func_801E3C34_59FB44(u16, u16, M2C_UNK);        /* extern */
extern unsigned char D_800C7DB2[];
extern f32 D_8020B1D0_5C70E0;
extern f32 D_8020B1D4_5C70E4;

void func_801DFE44_59BD54(void *arg0, void *arg1) {
    s32 temp_a2;
    u16 temp_v1;
    void *temp_v0;
    void *temp_v0_2;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    if (M2C_FIELD(temp_v0, u16 *, 0x30)++ == 0) {
        M2C_FIELD(arg0, f32 *, 0xE4) = (f32) D_8020B1D0_5C70E0;
        M2C_FIELD(arg0, f32 *, 0xE8) = (f32) D_8020B1D4_5C70E4;
        return;
    }
    M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xE8) = 1.0f;
    if ((((f32 (*)(void *))&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801DD6E0_5995F0(arg0, 0x16);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        if ((func_801E3C34_59FB44(M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u16 *, 8), M2C_FIELD(arg0, u16 *, 0x94), 0x100) != 0) && (*(u16 *)(D_800C7DB2 + (M2C_FIELD(arg0, u8 *, 0x90) * 0x18)) & 0x4000)) {
            temp_v0_2 = M2C_FIELD(arg0, void **, 0x5C);
            M2C_FIELD(temp_v0_2, u16 *, 2) = (u16) ((M2C_FIELD(temp_v0_2, u16 *, 2) + 0x200) & 0x3FF);
            func_801DACDC_596BEC(arg0, 0x4A);
            return;
        }
        func_801DACDC_596BEC(arg0, 0x47);
    }
}
