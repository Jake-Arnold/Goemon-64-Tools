typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
void func_801D8DE4_603864(s8 *);
void func_80038838_39438(s32);
void func_8000F000_FC00(s32, s32, s8 *);
s32 func_801DBA50_6064D0(s8 *, f32);
s32 func_801D8838_6032B8(s8 *, f32, f32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
f32 func_801D8910_603390(s8 *, M2C_UNK);          /* extern */
s32 func_801D8D7C_6037FC(s8 *);                   /* extern */
M2C_UNK func_8020552C_62FFAC();                     /* extern */
extern s8 *D_80214600_63F080;
extern M2C_UNK func_80202F70_62D9F0;

void func_80202E54_62D8D4(s8 *arg0, s8 *arg1) {
    s8 *sp24;

    sp24 = D_80214600_63F080 + 0x140;
    M2C_FIELD(arg0, f32 *, 0x74) = 12.0f;
    if (func_801DBA50_6064D0(arg0, -40.0f) != 0) {
        if (func_801D8838_6032B8(arg1, 80.0f, 22.0f) != 0) {
            func_8000F000_FC00(0x247, (s32) (D_80214600_63F080 + 0xA0), arg1);
        }
        if (func_801D8910_603390(arg0, 0x42A00000) == 0.0f) {
            M2C_FIELD(arg0, s8 *, 0x30) = 1;
            M2C_FIELD(arg0, s32 *, 0x48) = 0;
            M2C_FIELD(arg0, s8 *, 0x4C) = 0;
            func_8020552C_62FFAC();
            func_80034E8C_35A8C(&func_80202F70_62D9F0);
            return;
        }
        goto block_5;
    }
block_5:
    if ((func_801D8D7C_6037FC(arg0) == M2C_FIELD(D_80214600_63F080, s32 *, 0x1CC)) && (M2C_FIELD(sp24, u8 *, 0xE) == 0) && (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C5) == 0)) {
        M2C_FIELD(arg0, s8 *, 0x30) = 1;
        M2C_FIELD(arg0, s32 *, 0x48) = 0;
        M2C_FIELD(arg0, s8 *, 0x4C) = 0;
        func_80038838_39438(0x24A);
    }
    func_801D8DE4_603864(arg0);
}
