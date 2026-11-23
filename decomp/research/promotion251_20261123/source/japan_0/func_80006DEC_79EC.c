typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_80006DEC_79EC(void *arg0, void *arg1, s32 arg2) {
    s32 temp_a0;

    temp_a0 = osSetIntMask(1);
    (*(s32*)((u8*)(arg1) + 0x4)) = arg2;
    (*(s32*)((u8*)(arg1) + 0x0)) = (void *) (*(s32*)((u8*)(arg0) + 0x298));
    (*(s32*)((u8*)(arg0) + 0x298)) = arg1;
    osSetIntMask(temp_a0, arg1);
}
