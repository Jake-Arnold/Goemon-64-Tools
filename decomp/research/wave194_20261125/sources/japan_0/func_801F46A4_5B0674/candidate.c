typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801F46D8_5B06A8();                     /* extern */
extern M2C_UNK D_80209D20_5C5CF0;

void func_801F46A4_5B0674(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, M2C_UNK **, 0) = &D_80209D20_5C5CF0;
    M2C_FIELD(arg1, s8 *, 4) = 0;
    M2C_FIELD(arg1, s16 *, 6) = -1;
    func_801F46D8_5B06A8(arg0);
}
