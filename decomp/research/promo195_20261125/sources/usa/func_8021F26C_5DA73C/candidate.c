typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_80003E10_4A10(s32);
f32 func_80003EA0_4AA0(s32);
s32 func_802196FC_5D4BCC(void *, f32, f32, f32, s32);
void func_8021F26C_5DA73C(void *arg0, f32 arg1, u16 arg2, f32 arg3, f32 arg4) {
    void *sp24;

    sp24 = M2C_FIELD(arg0, void **, 0x18);
    func_802196FC_5D4BCC(arg0, arg3, 0.0f, arg4, (s32) arg2 / 2);
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) (func_80003E10_4A10((s32) M2C_FIELD(sp24, u16 *, 0x16)) * arg1);
    M2C_FIELD(arg0, f32 *, 0x80) = (f32) (func_80003EA0_4AA0((s32) M2C_FIELD(sp24, u16 *, 0x16)) * arg1);
}
