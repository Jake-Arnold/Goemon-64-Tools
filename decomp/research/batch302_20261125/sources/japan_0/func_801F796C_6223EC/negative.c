typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801D8DE4_603864(void *);
s32 func_801DBA50_6064D0(void *, f32);
f32 func_801D8660_6030E0(void *, f32);
s32 func_801FC8BC_62733C(void *, f32);
void func_8000F198_FD98(s32, s32, void *, f32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801FCC14_627694(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern s32 D_80214600_63F080;
extern M2C_UNK func_801F7A7C_6224FC;

void func_801F796C_6223EC(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    if ((func_801FC8BC_62733C(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 350.0f) != 0) && (M2C_FIELD(arg0, s32 *, 0x90) == 0)) {
        func_8000F198_FD98(0x281, D_80214600_63F080 + 0xA0, arg1, 1500.0f);
        func_801FCC14_627694(arg0, 0x3F000000, 0x3ECCCCCD, 0x3E99999A);
        M2C_FIELD(arg0, s32 *, 0x90) = 1;
    }
    if ((func_801DBA50_6064D0(arg0, -90.0f) != 0) && (func_801D8660_6030E0(arg1, 40.0f) == 0.0f)) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x3C;
        M2C_FIELD(arg0, f32 *, 0x70) = (f32) -M2C_FIELD(arg0, f32 *, 0x70);
        M2C_FIELD(arg0, f32 *, 0x78) = (f32) -M2C_FIELD(arg0, f32 *, 0x78);
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) | 2);
        M2C_FIELD(arg0, f32 *, 0x74) = 4.0f;
        func_801D8DE4_603864(arg0);
        func_80034E8C_35A8C(&func_801F7A7C_6224FC);
    }
}
