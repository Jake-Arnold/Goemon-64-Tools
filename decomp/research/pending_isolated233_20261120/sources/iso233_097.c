typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80212464_5CD934();
void func_8021242C_5CD8FC(void *arg0, s32 arg1) {
    (*(s32*)((u8*)(arg0) + 0x64)) = (s32) ((*(s32*)((u8*)(arg0) + 0x64)) | 2);
    func_8003521C_35E1C(&func_80212464_5CD934);
}
