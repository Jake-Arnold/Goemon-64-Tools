typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);      /* extern */
M2C_UNK func_801E01C8_59C198(void *, M2C_UNK);      /* extern */
M2C_UNK func_801E2A90_59EA60(void *, M2C_UNK);      /* extern */
M2C_UNK func_801ED260_5A9230();                     /* extern */
M2C_UNK func_801EDA24_5A99F4(void *, M2C_UNK);      /* extern */

void func_801EC90C_5A88DC(void *arg0) {
    u32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u8 *, 0x60);
    switch (temp_v0) {                              /* irregular */
    case 0:
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s8 *, 0x84) = 2;
        return;
    case 1:
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
        func_801E019C_59C16C(arg0, 0x8F);
        func_801ED260_5A9230();
        func_801EDA24_5A99F4(arg0, 0x22);
        func_801E2A90_59EA60(arg0, 0x19);
        func_80038838_39438(0x177);
        func_80038838_39438(0x178);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = 0.0f;
        return;
    case 3:
        M2C_FIELD(arg0, s8 *, 0x61) = 0;
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
        func_801E01C8_59C198(arg0, 0xAC);
        func_801ED260_5A9230();
        func_801EDA24_5A99F4(arg0, 0x22);
        func_80038838_39438(0x178);
        /* fallthrough */
    case 2:
        return;
    }
}
