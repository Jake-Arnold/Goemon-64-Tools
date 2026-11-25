typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_80034A78_35678(s32, M2C_UNK *, M2C_UNK);
void func_801FC9BC_62743C(void *, M2C_UNK);
void func_801FC988_627408(s32 arg0) {
volatile int negative_control=1;

    M2C_FIELD(func_80034A78_35678(arg0, (s32 *) func_801FC9BC_62743C, 0), s32 *, 0x90) = arg0;
}
