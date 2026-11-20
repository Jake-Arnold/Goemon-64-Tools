typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 D_80167C48_168848;
void func_8000C5E4_D1E4(s32 arg0, f32 arg1) {
    void *temp_v0;

    temp_v0 = *(&D_80167C48_168848 + arg0);
    if (temp_v0 != NULL) {
        (*(f32*)((u8*)(temp_v0) + 0x88)) = arg1;
    }
}
