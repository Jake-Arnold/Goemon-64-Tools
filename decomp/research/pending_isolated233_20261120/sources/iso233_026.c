typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_80168E84_169A84;
extern s32 D_80167170_167D70;
s32 func_80023880_24480(void) {
    osPfsRepairId(D_80168E84_169A84);
    (*(s32*)((u8*)(D_80168E84_169A84) + 0x3FC)) = osPfsInitPak(&D_80167170_167D70, D_80168E84_169A84, 0);
    return (*(s32*)((u8*)(D_80168E84_169A84) + 0x3FC));
}
