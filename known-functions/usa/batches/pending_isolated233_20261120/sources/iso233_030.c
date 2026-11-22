typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_80035430_36030(void *arg0, s32 arg1) {
    (*(s16*)((u8*)(arg0) + 0x24)) = (s16) ((*(s16*)((u8*)(arg0) + 0x24)) - 1);
    if ((*(s16*)((u8*)(arg0) + 0x24)) <= 0) {
        func_80035384_35F84();
    }
}
