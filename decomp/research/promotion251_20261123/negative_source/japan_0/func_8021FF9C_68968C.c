typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_8021FF9C_68968C(void *arg0, f32 arg1) {
 volatile unsigned int __native_negative_control = 0x13579BDFu;

    f32 temp_f0;
    
    void *temp_v0;
    void *temp_v1;

    (*(f32*)((u8*)((*(void**)((u8*)(arg0) + 0xB0))) + 0x24)) = arg1;
    temp_v0 = (*(s32*)((u8*)(arg0) + 0xB0));
    temp_f0 = (*(f32*)((u8*)(temp_v0) + 0x24));
    (*(f32*)((u8*)(temp_v0) + 0x20)) = temp_f0;
    (*(f32*)((u8*)((*(void**)((u8*)(arg0) + 0xB0))) + 0x1C)) = temp_f0;
    (*(f32*)((u8*)((*(void**)((u8*)(arg0) + 0xB4))) + 0x24)) = arg1;
    temp_v1 = (*(s32*)((u8*)(arg0) + 0xB4));
    temp_f0 = (*(f32*)((u8*)(temp_v1) + 0x24));
    (*(f32*)((u8*)(temp_v1) + 0x20)) = temp_f0;
    (*(f32*)((u8*)((*(void**)((u8*)(arg0) + 0xB4))) + 0x1C)) = temp_f0;
}
