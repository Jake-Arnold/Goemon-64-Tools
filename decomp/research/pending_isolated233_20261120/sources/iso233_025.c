typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_80168E84_169A84;
s32 func_800237F0_243F0(void) {
    s32 sp1C;
    s32 temp_v0;

    temp_v0 = osPfsNumFiles(D_80168E84_169A84, D_80168E84_169A84 + 0x400, D_80168E84_169A84 + 0x404);
    sp1C = temp_v0;
    func_80023ADC_246DC(temp_v0);
    (*(s32*)((u8*)(D_80168E84_169A84) + 0x3FC)) = sp1C;
    return (*(s32*)((u8*)(D_80168E84_169A84) + 0x3FC));
}
