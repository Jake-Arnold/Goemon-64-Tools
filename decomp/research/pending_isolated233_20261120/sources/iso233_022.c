typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 D_8015C5C8_15D1C8;
void func_80011C58_12858(void) {
    void *temp_v0;
    void *temp_v1;

    temp_v0 = (*(s32*)((u8*)(D_8015C5C8_15D1C8) + 0xCF8E8));
    if (temp_v0 != NULL) {
        (*(s16*)((u8*)(temp_v0) + 0x22)) = (u16) ((*(u16*)((u8*)(temp_v0) + 0x22)) & 0xFFEB);
        temp_v1 = (*(s32*)((u8*)((*(void**)((u8*)(D_8015C5C8_15D1C8) + 0xCF8E8))) + 0x18));
        (*(u8*)((u8*)(temp_v1) + 0x4)) = (u8) ((*(u8*)((u8*)(temp_v1) + 0x4)) & 0xFF7F);
    }
}
