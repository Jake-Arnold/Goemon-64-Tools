typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void * func_8003699C_3759C(s32, s32, s32, s32, s32, s32, s32);
void func_80036924_37524(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    if (arg4 >= 0) {
        func_8003699C_3759C(arg0, arg1, arg2, arg3, arg4, -1, 0);
        return;
    }
    func_8003699C_3759C(arg0, arg1, arg2, arg3, 0, 0, -arg4);
}
