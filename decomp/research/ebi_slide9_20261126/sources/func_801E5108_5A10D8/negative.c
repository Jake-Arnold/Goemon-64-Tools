typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef float f32; typedef double f64; typedef s32 M2C_UNK;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((u8 *)(expr)+(offset)))
extern char func_8001B13C_1BD3C;
void func_801E019C_59C16C(void *, int);
M2C_UNK func_801E2A90_59EA60(void *, M2C_UNK);      /* extern */
s32 func_801E8EB0_5A4E80(u16, u16, M2C_UNK);        /* extern */
extern f32 D_80210068_5CC038;
extern f32 D_8021006C_5CC03C;
extern unsigned char g_system[];

void func_801E5108_5A10D8(void *arg0, void *arg1) {
    s32 temp_a2;
    u16 temp_v1;
    void *temp_v0;
    void *temp_v0_2;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    temp_v1 = M2C_FIELD(temp_v0, u16 *, 0x30);
    temp_a2 = temp_v1 == 0;
    M2C_FIELD(temp_v0, u16 *, 0x30) = (u16) (temp_v1 + 1);
    if (temp_a2 != 0) {
        M2C_FIELD(arg0, f32 *, 0xE4) = (f32) D_80210068_5CC038;
        M2C_FIELD(arg0, f32 *, 0xE8) = (f32) D_8021006C_5CC03C;
        return;
    }
    M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xE8) = 1.0f;
    if ((((f32 (*)(void *))&func_8001B13C_1BD3C)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801E2A90_59EA60(arg0, 0x16);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        if ((func_801E8EB0_5A4E80(M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u16 *, 8), M2C_FIELD(arg0, u16 *, 0x94), 0x100) != 0) && (*(u16 *)(g_system + 0x3B0F2 + (M2C_FIELD(arg0, u8 *, 0x90) * 0x18)) & 0x4000)) {
            temp_v0_2 = M2C_FIELD(arg0, void **, 0x5C);
            M2C_FIELD(temp_v0_2, u16 *, 2) = (u16) ((M2C_FIELD(temp_v0_2, u16 *, 2) + 0x200) & 0x3FF);
            func_801E019C_59C16C(arg0, 0x4A);
            return;
        }
        func_801E019C_59C16C(arg0, 0x47);
    }
}
