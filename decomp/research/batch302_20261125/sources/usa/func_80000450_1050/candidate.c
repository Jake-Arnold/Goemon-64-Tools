typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK osCreateThread(M2C_UNK *, M2C_UNK, M2C_UNK *, M2C_UNK, M2C_UNK *, s32); /* extern */
M2C_UNK osInitialize();                             /* extern */
M2C_UNK osStartThread(M2C_UNK *);                   /* extern */
extern M2C_UNK D_80080020_80C20;
extern M2C_UNK D_800841D0_84DD0;
extern M2C_UNK func_800004AC_10AC;

void func_80000450_1050(void) {
    osInitialize();
    osCreateThread(&D_80080020_80C20, 1, &func_800004AC_10AC, 0, &D_800841D0_84DD0, 9);
    osStartThread(&D_80080020_80C20);
}
