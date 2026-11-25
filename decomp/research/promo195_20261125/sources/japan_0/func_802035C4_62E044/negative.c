typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_8000EAC0_F6C0(s32, void *);
M2C_UNK func_801D8738_6031B8(M2C_UNK, M2C_UNK);
M2C_UNK func_801D9238_603CB8(void *, M2C_UNK, M2C_UNK);
M2C_UNK func_801DBA50_6064D0(void *, M2C_UNK);
M2C_UNK func_801DC234_606CB4(void *, M2C_UNK);
M2C_UNK func_801DC2AC_606D2C(void *, M2C_UNK);
M2C_UNK func_80201B2C_62C5AC(void *);
extern void *D_80214600_63F080;

void func_802035C4_62E044(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t8;

    func_801D8738_6031B8(arg1, 0x42F00000);
    func_801D9238_603CB8(arg0, 0x42A00000, 4);
    if (func_8000EAC0_F6C0(M2C_FIELD(D_80214600_63F080, s32 *, 0x1CC), arg0) >= 200.0f) {
        func_801DC234_606CB4(arg0, 0x3CA3D70A);
        func_801DC2AC_606D2C(arg0, 0x3CA3D70A);
        M2C_FIELD(arg0, f32 *, 0x74) = 1.0f;
        func_801DBA50_6064D0(arg0, 0xC2C80000);
    }
    if (--M2C_FIELD(arg0, s32 *, 0x80) == 0) {
        func_80201B2C_62C5AC(arg0);
    }
}
