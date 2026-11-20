#define NULL ((void*)0)
 typedef unsigned char u8; typedef signed char s8; typedef unsigned short u16; typedef signed short s16; typedef unsigned int u32; typedef signed int s32; typedef unsigned long long u64; typedef signed long long s64; typedef float f32; typedef double f64;
void func_08000804_73C404(void *arg0) {
    s32 temp_v0;

    temp_v0 = (*(s32*)((u8*)arg0+0xD4));
    (*(s32*)((u8*)arg0+0xDC)) = temp_v0;
    (*(f32*)((u8*)arg0+0xE4)) = (f32) ((*(f32*)((u8*)arg0+0xE0)) / (f32) temp_v0);
}
