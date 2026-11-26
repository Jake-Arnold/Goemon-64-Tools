typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80217110_675F80(M2C_UNK, M2C_UNK, M2C_UNK, s32);
void func_80217190_676000(M2C_UNK, M2C_UNK, M2C_UNK, s32);
void func_80217210_676080(M2C_UNK, M2C_UNK, M2C_UNK, s32);
extern M2C_UNK D_80161DCC_1629CC;

void func_80218370_6771E0(s32 arg0, s32 arg1, s32 arg2) {
    func_80217110_675F80(arg0, arg1, arg2, M2C_FIELD(&D_80161DCC_1629CC, s32 *, 0x14));
    func_80217190_676000(arg0, arg1 + 0x1A, arg2, M2C_FIELD(&D_80161DCC_1629CC, s32 *, 0x18));
    func_80217210_676080(arg0, arg1 + 0x34, arg2, M2C_FIELD(&D_80161DCC_1629CC, s32 *, 0x20));
}
