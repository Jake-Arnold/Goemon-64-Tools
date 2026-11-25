typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801D8820_6032A0(char *, float);
void func_801D89C8_603448(void *arg0, f32 arg1) {
    if (arg0 != NULL) {
        func_801D8820_6032A0(M2C_FIELD(arg0, s8 **, 0x18), arg1);
    }
}
