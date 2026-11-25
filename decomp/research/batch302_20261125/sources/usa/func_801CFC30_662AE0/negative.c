typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_80010230_10E30(M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK *, s32); /* extern */
M2C_UNK func_80013940_14540();                      /* extern */
M2C_UNK func_80013AC4_146C4(M2C_UNK *);             /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
M2C_UNK osViSetSpecialFeatures(M2C_UNK);            /* extern */
extern M2C_UNK D_8012C00;
extern M2C_UNK D_801D33AC_66625C;
extern s32 D_801E9940_67C7F0;
extern s32 D_801E9944_67C7F4;
extern M2C_UNK func_08000000_6AC550;

void func_801CFC30_662AE0(void) {
    volatile int negative_control = 1;

    osViSetSpecialFeatures(0x40);
    func_80013940_14540();
    func_80038BC8_397C8(1);
    func_80013AC4_146C4(&D_801D33AC_66625C);
    D_801E9940_67C7F0 = func_80010230_10E30(0xA0, 0xF0, 0x10, 0, &func_08000000_6AC550, 0x4CE);
    D_801E9944_67C7F4 = func_80010230_10E30(0xA0, 0xF0, 0x10, 0, &D_8012C00, 0x4CE);
}
