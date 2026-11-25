typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80038BC8_397C8(s32);
void func_801D2EE4_5FE2C4(void *, void *);
void func_801D34D0_5FE8B0(void *, s32, s32, s32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern M2C_UNK D_8020B094_636474;
extern M2C_UNK D_8020B188_636568;
extern M2C_UNK func_801E8488_613868;

void func_801E8368_613748(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0xB0) = 0;
    M2C_FIELD(arg0, f32 *, 0x74) = 7.0f;
    func_801D2EE4_5FE2C4(arg1, &D_8020B188_636568);
    func_801D34D0_5FE8B0(arg1, (s32) &D_8020B094_636474, 0, 1);
    func_80038BC8_397C8(0x34E);
    M2C_FIELD(arg0, s32 *, 0xE8) = (s32) (M2C_FIELD(arg0, s32 *, 0xE8) + 1);
    func_8003521C_35E1C(&func_801E8488_613868);
}
