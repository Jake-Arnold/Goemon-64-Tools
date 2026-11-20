#define NULL ((void*)0)
 typedef unsigned char u8; typedef signed char s8; typedef unsigned short u16; typedef signed short s16; typedef unsigned int u32; typedef signed int s32; typedef unsigned long long u64; typedef signed long long s64; typedef float f32; typedef double f64;
void func_08001434_70B474(void *arg0, f32 *arg1, f32 *arg2, f32 *arg3) {
    void *temp_v0;

    temp_v0 = (*(s32*)((u8*)arg0+0x18));
    *arg1 = (*(f32*)((u8*)temp_v0+0x8));
    *arg2 = (*(f32*)((u8*)temp_v0+0xC));
    *arg3 = (*(f32*)((u8*)temp_v0+0x10));
}
