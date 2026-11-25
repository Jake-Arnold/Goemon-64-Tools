typedef signed char s8; typedef unsigned char u8; typedef short s16; typedef unsigned short u16; typedef int s32; typedef unsigned int u32; typedef long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64;
s32 func_8002338C_23F8C(void) { return 0; }
#define BATCH302_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
extern s32 func_80023ADC_246DC(s32);
extern s32 D_80168E84_169A84;
extern s32 osPfsAllocateFile(s8 *, s32, s32, s32 *, s32 *, s32, s8 *);
extern s32 D_8006D170_6DD70, D_80168A00_169600;
s32 func_80023394_23F94(void) {
    s32 temp_v0;
    s32 sp2C;
    s32 var_a0;

    temp_v0 = osPfsAllocateFile((s8 *)D_80168E84_169A84, 0x4134, 0x4E473545, &D_8006D170_6DD70, &D_80168A00_169600, 0x1000, (s8 *)D_80168E84_169A84 + 0x3F0);
    var_a0 = temp_v0;
    if (temp_v0 != 0) {
        sp2C = temp_v0;
        func_80023ADC_246DC(var_a0);
        var_a0 = sp2C;
    }
    BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3FC) = var_a0;
    return BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3FC);
}
#undef BATCH302_FIELD
/* Original native C for func_80023410_24010 */
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

#define BATCH302_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
extern s32 func_80023ADC_246DC(s32);
extern s32 D_80168E84_169A84;
extern s32 osPfsFileState(void *, s32, void *);
s32 func_80023480_24080(void) {
    s32 sp1C;
    s32 temp_a1;
    s32 temp_v0;

    temp_a1 = BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3F0);
    temp_v0 = osPfsFileState((void *)D_80168E84_169A84, temp_a1, ((s8 *)D_80168E84_169A84) + (temp_a1 << 5) + 0x1B0);
    sp1C = temp_v0;
    func_80023ADC_246DC(temp_v0);
    BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3FC) = sp1C;
    return BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3FC);
}
#undef BATCH302_FIELD
#define BATCH302_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
extern s32 func_80023ADC_246DC(s32);
extern s32 D_80168E84_169A84;
extern s32 osPfsReadWriteFile(void *, s32, s32, s32, s32, s32);
s32 func_800234D8_240D8(s32 arg0, s32 arg1) {
    s32 sp24;
    s32 temp_v0;

    BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3F4) = arg0;
    temp_v0 = osPfsReadWriteFile((void *)D_80168E84_169A84, BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3F0), 0, (arg1 * 0x500) + 0x100, 0x500, BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3F4));
    sp24 = temp_v0;
    func_80023ADC_246DC(temp_v0);
    BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3FC) = sp24;
    return BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3FC);
}
#undef BATCH302_FIELD
#pragma GLOBAL_ASM("asm/usa/nonmatchings/return_zero/func_80023560_24160.s")
#define BATCH302_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
extern s32 func_80023ADC_246DC(s32);
extern s32 D_80168E84_169A84;
extern s32 osPfsReadWriteFile(void *, s32, s32, s32, s32, s32);
s32 func_80023610_24210(s32 arg0, s32 arg1) {
    s32 sp24;
    s32 temp_v0;

    BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3F4) = arg0;
    temp_v0 = osPfsReadWriteFile((void *)D_80168E84_169A84, BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3F0), 1, (arg1 * 0x500) + 0x100, 0x500, BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3F4));
    sp24 = temp_v0;
    func_80023ADC_246DC(temp_v0);
    BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3FC) = sp24;
    return BATCH302_FIELD(D_80168E84_169A84, s32 *, 0x3FC);
}
#undef BATCH302_FIELD
#pragma GLOBAL_ASM("asm/usa/nonmatchings/return_zero/func_80023698_24298.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/return_zero/func_80023788_24388.s")
/* Original native C for func_800237F0_243F0 */
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

s32 osPfsIsPlug(s32 *, u8 *);                   /* extern */
extern s32 D_80167170_167D70;

s32 func_80023840_24440(void) {
    u8 sp1F;

    if (osPfsIsPlug(&D_80167170_167D70, &sp1F) == -1) {
        return -1;
    }
    return sp1F & 1;
}
/* Original native C for func_80023880_24480 */
extern s32 D_80168E84_169A84;
extern s32 D_80167170_167D70;
s32 func_80023880_24480(void) {
    osPfsRepairId(D_80168E84_169A84);
    (*(s32*)((u8*)(D_80168E84_169A84) + 0x3FC)) = osPfsInitPak(&D_80167170_167D70, D_80168E84_169A84, 0);
    return (*(s32*)((u8*)(D_80168E84_169A84) + 0x3FC));
}

#pragma GLOBAL_ASM("asm/usa/nonmatchings/return_zero/func_800238D0_244D0.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/return_zero/func_800239B8_245B8.s")
