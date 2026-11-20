#define NULL ((void*)0)
 typedef unsigned char u8; typedef signed char s8; typedef unsigned short u16; typedef signed short s16; typedef unsigned int u32; typedef signed int s32; typedef unsigned long long u64; typedef signed long long s64; typedef float f32; typedef double f64;
u8 func_801D3854_5FEC34(void *arg0) {
    void *temp_v1;

    temp_v1 = (*(s32*)((u8*)arg0+0x38));
    if (temp_v1 != NULL) {
        return (*(u8*)((u8*)temp_v1+0x4C));
    }
    return 0U;
}
