typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
M2C_UNK func_801DACDC_596BEC(void *, M2C_UNK);      /* extern */
M2C_UNK func_801DCCF0_598C00(M2C_UNK);              /* extern */
M2C_UNK func_801DD6E0_5995F0(void *, M2C_UNK);      /* extern */
M2C_UNK func_801E307C_59EF8C(void *);               /* extern */
M2C_UNK func_801E3278_59F188(void *);               /* extern */
M2C_UNK func_801E77A4_5A36B4();                     /* extern */
M2C_UNK func_801E8160_5A4070();                     /* extern */
M2C_UNK func_801E8964_5A4874(void *, M2C_UNK);      /* extern */
extern f32 D_8020B5D0_5C74E0;

void func_801E75D4_5A34E4(void *arg0) {
    s32 temp_v0;

    func_801E77A4_5A36B4();
    temp_v0 = M2C_FIELD(arg0, u8 *, 0x60);
    switch (temp_v0) {                              /* irregular */
    case 0:
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        func_801DACDC_596BEC(arg0, 0x82);
        func_801DCCF0_598C00(-0xA);
        M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
        func_801E307C_59EF8C(arg0);
        func_801E8160_5A4070();
        func_80038BC8_397C8(0x173);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = 0.0f;
        return;
    case 1:
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
        func_801E307C_59EF8C(arg0);
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
        func_801DACDC_596BEC(arg0, 0x8E);
        func_801E8160_5A4070();
        func_801E8964_5A4874(arg0, 0x22);
        func_80038BC8_397C8(0x172);
        func_80038BC8_397C8(0x178);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = 0.0f;
        return;
    case 2:
        func_801E3278_59F188(arg0);
        M2C_FIELD(arg0, f32 *, 0xA4) = 2.5f;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = (f32) D_8020B5D0_5C74E0;
        M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s8 *, 0x2E) = 0;
        func_801DD6E0_5995F0(arg0, 0x21);
        func_801DACDC_596BEC(arg0, 0x9B);
        func_801E8964_5A4874(arg0, 0x16);
        func_80038BC8_397C8(0x14F);
        func_801DD6E0_5995F0(arg0, 0x19);
        return;
    case 3:
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
        func_801DACDC_596BEC(arg0, 0xAA);
        func_801E8160_5A4070();
        func_801E8964_5A4874(arg0, 0x22);
        func_80038BC8_397C8(0x178);
        M2C_FIELD(arg0, f32 *, 0xA4) = 0.0f;
        return;
    }
}
