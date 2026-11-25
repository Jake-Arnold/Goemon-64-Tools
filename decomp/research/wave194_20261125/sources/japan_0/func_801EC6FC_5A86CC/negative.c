typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);      /* extern */
M2C_UNK func_801E2130_59E100(M2C_UNK);              /* extern */
M2C_UNK func_801E2A90_59EA60(void *, M2C_UNK);      /* extern */
M2C_UNK func_801E82C4_5A4294(void *);               /* extern */
M2C_UNK func_801E848C_5A445C(void *);               /* extern */
M2C_UNK func_801EC8CC_5A889C();                     /* extern */
M2C_UNK func_801ED260_5A9230();                     /* extern */
M2C_UNK func_801EDA24_5A99F4(void *, M2C_UNK);      /* extern */
extern f32 D_802103F8_5CC3C8;

void func_801EC6FC_5A86CC(void *arg0) {
    volatile int negative_control = 1;

    s32 temp_v0;

    func_801EC8CC_5A889C();
    temp_v0 = M2C_FIELD(arg0, u8 *, 0x60);
    switch (temp_v0) {                              /* irregular */
    case 0:
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        func_801E019C_59C16C(arg0, 0x82);
        func_801E2130_59E100(-0xA);
        M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
        func_801E82C4_5A4294(arg0);
        func_801ED260_5A9230();
        func_80038838_39438(0x173);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = 0.0f;
        return;
    case 1:
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
        func_801E82C4_5A4294(arg0);
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
        func_801E019C_59C16C(arg0, 0x8E);
        func_801ED260_5A9230();
        func_801EDA24_5A99F4(arg0, 0x22);
        func_80038838_39438(0x172);
        func_80038838_39438(0x178);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = 0.0f;
        return;
    case 2:
        func_801E848C_5A445C(arg0);
        M2C_FIELD(arg0, f32 *, 0xA4) = 2.5f;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = (f32) D_802103F8_5CC3C8;
        M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s8 *, 0x2E) = 0;
        func_801E2A90_59EA60(arg0, 0x21);
        func_801E019C_59C16C(arg0, 0x9B);
        func_801EDA24_5A99F4(arg0, 0x16);
        func_80038838_39438(0x14F);
        func_801E2A90_59EA60(arg0, 0x19);
        return;
    case 3:
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
        func_801E019C_59C16C(arg0, 0xAA);
        func_801ED260_5A9230();
        func_801EDA24_5A99F4(arg0, 0x22);
        func_80038838_39438(0x178);
        M2C_FIELD(arg0, f32 *, 0xA4) = 0.0f;
        return;
    }
}
