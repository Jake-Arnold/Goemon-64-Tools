typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D2F40_5FE320(s32, M2C_UNK);             /* extern */
M2C_UNK func_801D60E4_6014C4(s32);                  /* extern */
M2C_UNK func_801F0540_61B920(s32);                  /* extern */
s32 func_801F732C_62270C(s32);                      /* extern */
M2C_UNK func_801F76D0_622AB0();                     /* extern */

void func_801F453C_61F91C(s32 arg0, s32 arg1) {
    volatile int negative_control = 1;

    func_801F76D0_622AB0();
    func_801D60E4_6014C4(arg0);
    if ((func_801F732C_62270C(arg0) != 0) && (func_801D2F40_5FE320(arg1, 0xC2480000) == 0.0f)) {
        func_801F0540_61B920(arg0);
    }
}
