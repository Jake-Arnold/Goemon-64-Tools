typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_801E3324_59F234(void *arg0) {
    (*(s16*)((u8*)((*(void**)((u8*)(arg0) + 0x5C))) + 0x0)) = 0;
    if ((*(u8*)((u8*)(arg0) + 0x60)) == 1) {
        (*(u8*)((u8*)(arg0) + 0xDB)) = 0;
    } else {
        (*(u8*)((u8*)(arg0) + 0xDB)) = 1;
    }
    (*(s16*)((u8*)((*(void**)((u8*)(arg0) + 0x5C))) + 0x30)) = 0;
}
