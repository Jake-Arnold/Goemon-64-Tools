typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801D31F0_5FE5D0(s32, M2C_UNK);              /* extern */
M2C_UNK func_801F0540_61B920(s32);                  /* extern */
M2C_UNK func_801F72B4_622694(s32, M2C_UNK, M2C_UNK); /* extern */
extern void *D_8020EED0_63A2B0;

void func_801EF8C8_61ACA8(s32 arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    func_801D31F0_5FE5D0(arg0, 0x42200000);
    func_801F72B4_622694(arg0, 0x3CA3D70A, 0x3ECCCCCD);
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C0) == 0) {
        func_801F0540_61B920(arg0);
    }
}
