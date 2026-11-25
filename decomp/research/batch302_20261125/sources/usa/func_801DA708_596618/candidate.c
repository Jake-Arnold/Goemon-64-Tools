typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801DA758_596668();                     /* extern */
extern f32 D_8020AF28_5C6E38;

void func_801DA708_596618(void *arg0) {
    func_801DA758_596668();
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = (f32) D_8020AF28_5C6E38;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0) = 0;
    M2C_FIELD(arg0, s16 *, 0xCE) = 0;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x34) = 0;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 2) = 0;
}
