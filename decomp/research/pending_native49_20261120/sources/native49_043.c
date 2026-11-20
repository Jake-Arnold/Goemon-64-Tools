#define NULL ((void*)0)
 typedef unsigned char u8; typedef signed char s8; typedef unsigned short u16; typedef signed short s16; typedef unsigned int u32; typedef signed int s32; typedef unsigned long long u64; typedef signed long long s64; typedef float f32; typedef double f64;
void func_08000F50_72A4F0(void *arg0, f32 arg1, f32 arg2, f32 arg3) {
    (*(f32*)((u8*)arg0+0xE0)) = arg1;
    (*(f32*)((u8*)arg0+0xE4)) = arg2;
    (*(f32*)((u8*)arg0+0xE8)) = arg3;
}
