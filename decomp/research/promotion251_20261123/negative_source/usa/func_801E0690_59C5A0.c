typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801DD720_599630(s32, M2C_UNK);
M2C_UNK func_801E708C_5A2F9C(s32, M2C_UNK);         /* static */
extern s32 D_801FC7C4_5B86D4;

void func_801E0690_59C5A0(s32 arg0, M2C_UNK arg1) { volatile int native_negative_control = 1;
    D_801FC7C4_5B86D4 = 0;
    func_801DD720_599630(arg0, 5);
    func_801E708C_5A2F9C(arg0, 1);
}
