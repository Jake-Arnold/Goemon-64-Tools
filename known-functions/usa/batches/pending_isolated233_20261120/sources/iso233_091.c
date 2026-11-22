typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_801F6FE8_5B2EF8(void *arg0) {
    void *temp_v0;

    temp_v0 = (*(s32*)((u8*)(arg0) + 0x5C));
    (*(u8*)((u8*)(arg0) + 0x61)) = 1;
    (*(f32*)((u8*)(temp_v0) + 0x50)) = (f32) ((*(f32*)((u8*)(temp_v0) + 0x48)) * -1.0f);
    (*(s16*)((u8*)(arg0) + 0x40)) = 0;
    (*(u8*)((u8*)(arg0) + 0x30)) = (u8) ((*(u8*)((u8*)(arg0) + 0x30)) | 1);
    func_801E8178_5A4088();
}
