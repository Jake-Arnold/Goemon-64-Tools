typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80035DFC_369FC(s32, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_80036660_37260();                      /* extern */
extern s32 D_8006D320_6DF20;
extern u16 D_8016DAB0_16E6B0;

void func_800367E4_373E4(s32 arg0) {
    if (arg0 != 0) {
        func_80036660_37260();
        D_8016DAB0_16E6B0 -= 1;
        if (D_8006D320_6DF20 != 0) {
            func_80035DFC_369FC(D_8006D320_6DF20, 2, 1);
        }
    }
}
