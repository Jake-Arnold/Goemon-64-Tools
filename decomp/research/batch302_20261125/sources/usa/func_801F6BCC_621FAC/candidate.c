typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D2F40_5FE320(s32, M2C_UNK);             /* extern */
s32 func_801D6C4C_60202C(void *, M2C_UNK);          /* extern */
M2C_UNK func_801F0540_61B920(void *);               /* extern */
M2C_UNK func_801F732C_62270C();                     /* extern */

void func_801F6BCC_621FAC(void *arg0, s32 arg1) {
    func_801F732C_62270C();
    if ((func_801D2F40_5FE320(arg1, 0xC1A00000) == 0.0f) && (func_801D6C4C_60202C(arg0, 0x3E4CCCCD) != 0)) {
        if (M2C_FIELD(arg0, s32 *, 0xEC) > 0) {
            M2C_FIELD(arg0, s32 *, 0xEC) = 0;
            M2C_FIELD(arg0, s32 *, 0xD4) = 0;
        }
        func_801F0540_61B920(arg0);
    }
}
