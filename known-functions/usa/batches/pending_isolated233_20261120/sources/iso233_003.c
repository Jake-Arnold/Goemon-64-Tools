typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_8000777C_837C(void *arg0) {
    void *temp_v0;

    temp_v0 = (*(s32*)((u8*)(arg0) + 0x2AC));
    if ((*(s32*)((u8*)(temp_v0) + 0x10)) == 1) {
        (*(s32*)((u8*)(temp_v0) + 0x4)) = (s32) ((*(s32*)((u8*)(temp_v0) + 0x4)) | 0x10);
        osSpTaskYield();
    }
}
