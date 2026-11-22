typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80219E70_5D5340();
extern s32 func_802253A8_5E0878();
extern s32 func_80225954_5E0E24();
void func_802259D8_5E0EA8(void *arg0, s32 arg1) {
    void *sp1C;

    sp1C = (*(s32*)((u8*)(arg0) + 0x18));
    if (func_802253A8_5E0878() != 0) {
        (*(s32*)((u8*)(arg0) + 0x60)) = 0x12800761;
        (*(s32*)((u8*)(arg0) + 0x64)) = 0x20;
        (*(s16*)((u8*)(arg0) + 0xE4)) = (s16) (s32) (*(f32*)((u8*)(sp1C) + 0xC));
        func_80219E70_5D5340(arg0, 5, 0);
        func_8003521C_35E1C(&func_80225954_5E0E24);
    }
}
