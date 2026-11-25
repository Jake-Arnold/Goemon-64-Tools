typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_80003E10_4A10(u16);                        /* extern */
f32 func_80003EA0_4AA0(u16);                        /* extern */
s32 func_8000DD58_E958(M2C_UNK);                    /* extern */
M2C_UNK func_8003522C_35E2C(void *, M2C_UNK *);     /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801F7004_6223E4();                     /* extern */
M2C_UNK func_801F7074_622454(void *);               /* extern */
extern M2C_UNK D_8020B278_636658;
extern M2C_UNK func_801F07E4_61BBC4;

void func_801F0690_61BA70(void *arg0, s32 arg1) {
    void *sp24;
    f32 temp_f2;

    func_801F7004_6223E4();
    func_801F7074_622454(arg0);
    sp24 = M2C_FIELD(arg0, void **, 0x18);
    func_801D31CC_5FE5AC(arg0, &D_8020B278_636658);
    M2C_FIELD(arg0, f32 *, 0x70) = (f32) ((f64) func_80003E10_4A10(M2C_FIELD(sp24, u16 *, 0x16)) * 5.0);
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) ((f64) func_80003EA0_4AA0(M2C_FIELD(sp24, u16 *, 0x16)) * 5.0);
    temp_f2 = M2C_FIELD(sp24, f32 *, 8);
    if (temp_f2 >= 450.0f) {
        M2C_FIELD(arg0, f32 *, 0xB0) = -500.0f;
    } else if (temp_f2 <= -450.0f) {
        M2C_FIELD(arg0, f32 *, 0xB0) = 500.0f;
    } else if (func_8000DD58_E958(0x64) < 0x33) {
        M2C_FIELD(arg0, f32 *, 0xB0) = 500.0f;
    } else {
        M2C_FIELD(arg0, f32 *, 0xB0) = -500.0f;
    }
    M2C_FIELD(arg0, f32 *, 0xB8) = (f32) (func_8000DD58_E958(0xC8) - 0x258);
    M2C_FIELD(arg0, s32 *, 0x7C) = arg1;
    func_8003522C_35E2C(arg0, &func_801F07E4_61BBC4);
}
