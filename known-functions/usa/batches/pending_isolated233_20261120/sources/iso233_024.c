typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_80168A00_169600;
extern s32 D_8006D170_6DD70;
extern s32 D_80168E84_169A84;
s32 func_80023410_24010(void) {
    s32 sp24;
    s32 temp_v0;

    temp_v0 = osPfsFindFile(D_80168E84_169A84, 0x4134, 0x4E473545, &D_8006D170_6DD70, &D_80168A00_169600, D_80168E84_169A84 + 0x3F0);
    sp24 = temp_v0;
    func_80023ADC_246DC(temp_v0);
    (*(s32*)((u8*)(D_80168E84_169A84) + 0x3FC)) = sp24;
    return (*(s32*)((u8*)(D_80168E84_169A84) + 0x3FC));
}
