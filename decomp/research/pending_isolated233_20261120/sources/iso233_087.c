typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL 0
extern s32 func_80038BC8_397C8();
void func_801EDBB8_5A9AC8(void *arg0) {
    void *temp_v0;

    temp_v0 = (*(s32*)((u8*)(arg0) + 0x38));
    if ((temp_v0 != NULL) && ((*(u8*)((u8*)(temp_v0) + 0x4C)) == 6)) {
        func_80038BC8_397C8(0x23B, arg0);
    }
    (*(s32*)((u8*)(arg0) + 0x38)) = NULL;
    (*(s32*)((u8*)(arg0) + 0x34)) = 0;
}
