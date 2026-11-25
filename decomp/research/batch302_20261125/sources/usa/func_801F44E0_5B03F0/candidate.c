typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801E3B9C_59FAAC(s32, M2C_UNK);         /* extern */
M2C_UNK func_801E3D04_59FC14(s32, M2C_UNK);         /* extern */
s32 func_801F4984_5B0894(s32, M2C_UNK);                  /* extern */

void func_801F44E0_5B03F0(s32 arg0, M2C_UNK arg1) {
    if (func_801F4984_5B0894(arg0, 0x71) != 0) {
        func_801E3B9C_59FAAC(arg0, 0xBF19999A);
        func_801E3D04_59FC14(arg0, 0x10);
    }
}
