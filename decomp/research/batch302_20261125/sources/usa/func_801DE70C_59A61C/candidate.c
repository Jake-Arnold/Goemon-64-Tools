typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801E3EBC_59FDCC(s32, M2C_UNK, f32);    /* extern */
s32 func_801E7DE8_5A3CF8();                         /* extern */
extern f32 D_8020B18C_5C709C;

void func_801DE70C_59A61C(s32 arg0, M2C_UNK arg1) {
    f32 var_f0;

    if (func_801E7DE8_5A3CF8() != 0) {
        var_f0 = D_8020B18C_5C709C;
    } else {
        var_f0 = 4.0f;
    }
    func_801E3EBC_59FDCC(arg0, 0x21, var_f0);
}
