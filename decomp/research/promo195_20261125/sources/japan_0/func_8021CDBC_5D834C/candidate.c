typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void * func_8021BF18_5D74A8(void *, s32, s32);
extern M2C_UNK func_80216D48_5D22D8;
extern M2C_UNK func_80218778_5D3D08;

void func_8021CDBC_5D834C(void *arg0, s32 arg1) {
    if (arg1 != 0) {
        func_8021BF18_5D74A8(arg0, (s32) &func_80218778_5D3D08, 0xD);
        return;
    }
    func_8021BF18_5D74A8(arg0, (s32) &func_80216D48_5D22D8, 8);
}
