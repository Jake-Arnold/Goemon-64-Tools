typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_80037890_38490(s32, s32, s32);
u8 func_801DC150_606BD0(void *, f32, f32, f32);
void func_801D8604_603084(void *, void *);
f32 func_801D8910_603390(void *, M2C_UNK);
void func_801FCE00_627880(void *);
void func_800388A0_394A0(s32, s32, s32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_8003790C_3850C(M2C_UNK, M2C_UNK);      /* extern */
extern M2C_UNK D_80210A00_63B480;
extern void *D_80214600_63F080;
extern M2C_UNK func_801F5434_61FEB4;

void func_801F5364_61FDE4(void *arg0, void *arg1) {
    func_801FCE00_627880(arg0);
    func_801D8910_603390(arg0, 0x42A00000);
    func_801DC150_606BD0(arg0, -135.0f, 0.02f, 0.4f);
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) == 2) {
        func_8003790C_3850C(0, 0x64);
        func_80037890_38490(0, 1, 0x33333333);
        func_801D8604_603084(arg1, &D_80210A00_63B480);
        M2C_FIELD(arg0, f32 *, 0x74) = 7.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = -3.0f;
        func_800388A0_394A0(0x153, 0x40, 0xC0);
        func_80034E8C_35A8C(&func_801F5434_61FEB4);
    }
}
