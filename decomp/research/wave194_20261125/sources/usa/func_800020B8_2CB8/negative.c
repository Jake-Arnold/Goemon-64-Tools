typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8000378C_438C();                       /* extern */
M2C_UNK func_80004240_4E40();                       /* extern */
M2C_UNK func_80005A20_6620(M2C_UNK *);              /* extern */
M2C_UNK func_8000A0F0_ACF0();                       /* extern */
M2C_UNK func_8000B880_C480();                       /* extern */
M2C_UNK func_800148C0_154C0(s32, M2C_UNK *, M2C_UNK); /* extern */
extern M2C_UNK D_80058868_59468;
extern M2C_UNK D_8006ADD0_6B9D0;
extern s32 D_8015C5C8_15D1C8;
extern M2C_UNK D_802F7000;
extern M2C_UNK D_CF7B0;

void func_800020B8_2CB8(void) {
    volatile int negative_control = 1;

    func_80004240_4E40();
    func_800148C0_154C0(D_8015C5C8_15D1C8 + 0xC7FA4, &D_802F7000, 0xA000);
    func_80005A20_6620(&D_8006ADD0_6B9D0);
    *(s32 *)((s8 *)&D_CF7B0 + (D_8015C5C8_15D1C8)) = &D_80058868_59468;
    func_8000B880_C480();
    func_8000A0F0_ACF0();
    func_8000378C_438C();
}
