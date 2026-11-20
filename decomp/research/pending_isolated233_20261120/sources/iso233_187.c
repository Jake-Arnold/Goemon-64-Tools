typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_801E0228_64F078(void *arg0, void *arg1) {
    void *temp_v0;
    void *temp_v1;

    temp_v0 = (*(s32*)((u8*)(arg0) + 0x6C));
    (*(f32*)((u8*)(arg0) + 0x7C)) = (f32) (*(f32*)((u8*)(temp_v0) + 0x5C));
    (*(f32*)((u8*)(arg0) + 0x80)) = (f32) (*(f32*)((u8*)(temp_v0) + 0x60));
    (*(f32*)((u8*)(arg0) + 0x84)) = (f32) (*(f32*)((u8*)(temp_v0) + 0x64));
    temp_v1 = (*(s32*)((u8*)(temp_v0) + 0x18));
    (*(s16*)((u8*)(arg0) + 0x72)) = (u16) (*(u16*)((u8*)(temp_v1) + 0x14));
    (*(s16*)((u8*)(arg0) + 0x74)) = (u16) (*(u16*)((u8*)(temp_v1) + 0x16));
    (*(s16*)((u8*)(arg0) + 0x76)) = (u16) (*(u16*)((u8*)(temp_v1) + 0x18));
    (*(f32*)((u8*)(arg1) + 0x88)) = (f32) (*(f32*)((u8*)(arg0) + 0x88));
    (*(f32*)((u8*)(arg1) + 0x8C)) = (f32) (*(f32*)((u8*)(arg0) + 0x8C));
    (*(f32*)((u8*)(arg1) + 0x90)) = (f32) (*(f32*)((u8*)(arg0) + 0x90));
}
