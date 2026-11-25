typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_80010230_10E30(M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK *, s32); /* extern */
M2C_UNK func_80013AC4_146C4(M2C_UNK *);             /* extern */
extern M2C_UNK D_80131B0;
extern M2C_UNK D_80216F5C_675F0C;
extern s32 D_8021E480_67D430;
extern s32 D_8021E484_67D434;
extern s32 D_8021E488_67D438;
extern M2C_UNK D_80305B0;
extern M2C_UNK D_80315B0;

void func_802144E0_673490(void) {
    volatile int negative_control = 1;

    func_80013AC4_146C4(&D_80216F5C_675F0C);
    D_8021E480_67D430 = func_80010230_10E30(0x120, 0xD0, 0x10, 0, &D_80131B0, 0x4D2);
    D_8021E484_67D434 = func_80010230_10E30(0x40, 0x20, 0x10, 0, &D_80305B0, 0x4D2);
    D_8021E488_67D438 = func_80010230_10E30(0x40, 0x20, 0x10, 0, &D_80315B0, 0x4D2);
}
