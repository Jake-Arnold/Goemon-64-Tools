typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_80226764_5E1C34(void *arg0) {
    void *sp1C;

    (*(s32*)((u8*)(arg0) + 0x60)) = 0x261;
    (*(s32*)((u8*)(arg0) + 0x64)) = 0x20;
    sp1C = (*(s32*)((u8*)(arg0) + 0x18));
    func_80225BB8_5E1088();
    (*(s16*)((u8*)(arg0) + 0xE4)) = (s16) (s32) (*(f32*)((u8*)(sp1C) + 0xC));
    func_80219E70_5D5340(arg0, 5, 0);
}
