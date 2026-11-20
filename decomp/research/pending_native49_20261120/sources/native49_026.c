#define NULL ((void*)0)
 typedef unsigned char u8; typedef signed char s8; typedef unsigned short u16; typedef signed short s16; typedef unsigned int u32; typedef signed int s32; typedef unsigned long long u64; typedef signed long long s64; typedef float f32; typedef double f64;
void func_80210688_698088(void *arg0, s32 arg1) {
    void *temp_v0;

    temp_v0 = (*(s32*)((u8*)arg0+0x18));
    (*(s32*)((u8*)temp_v0+0x50)) = (s32) ((*(s32*)((u8*)temp_v0+0x38)) + arg1 + 0xF8000000);
}
