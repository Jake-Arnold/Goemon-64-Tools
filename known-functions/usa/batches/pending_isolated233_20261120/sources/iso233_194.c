typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_80014B74_15774();
extern s32 func_80034EF8_35AF8();
extern s32 D_8015C5C8_15D1C8;
void func_802111C4_670174(void *arg0) {
    s32 temp_a1;

    if (arg0 != NULL) {
        temp_a1 = (*(s32*)((u8*)(arg0) + 0x5C));
        if (temp_a1 != 0) {
            func_80014B74_15774(D_8015C5C8_15D1C8 + 0xC7FA4, temp_a1, arg0);
        }
        func_80034EF8_35AF8(arg0);
    }
}
