typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801DD720_599630(s32, M2C_UNK);
M2C_UNK func_801E50C0_5A0FD0(s32);                  /* static */

void func_801DEB50_59AA60(s32 arg0, M2C_UNK arg1) { volatile int native_negative_control = 1;
    func_801DD720_599630(arg0, 0xC);
    func_801E50C0_5A0FD0(arg0);
}
