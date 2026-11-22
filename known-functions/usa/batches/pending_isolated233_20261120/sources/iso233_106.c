typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_8015CC30_15D830;
void func_8021893C_5D3E0C(void *arg0) {
    void *temp_v0;

    temp_v0 = (*(s32*)((u8*)(arg0) + 0x18));
    if ((*(s32*)((u8*)(arg0) + 0x60)) & 0x10000000) {
        (*(f32*)((u8*)(&D_8015CC30_15D830)+0x74)) = (f32) (*(f32*)((u8*)(temp_v0) + 0x8));
        (*(f32*)((u8*)(&D_8015CC30_15D830)+0x78)) = (f32) (*(f32*)((u8*)(temp_v0) + 0xC));
        (*(f32*)((u8*)(&D_8015CC30_15D830)+0x7C)) = (f32) (*(f32*)((u8*)(temp_v0) + 0x10));
        (*(f32*)((u8*)(&D_8015CC30_15D830)+0x80)) = (f32) (*(f32*)((u8*)(arg0) + 0x78));
        (*(f32*)((u8*)(&D_8015CC30_15D830)+0x84)) = (f32) (*(f32*)((u8*)(arg0) + 0x7C));
        (*(f32*)((u8*)(&D_8015CC30_15D830)+0x88)) = (f32) (*(f32*)((u8*)(arg0) + 0x80));
    }
}
