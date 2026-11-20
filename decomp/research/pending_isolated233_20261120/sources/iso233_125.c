typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_80219E70_5D5340();
extern s32 func_8021C654_5D7B24();
extern s32 func_802253A8_5E0878();
extern s32 func_802258BC_5E0D8C();
void func_802258FC_5E0DCC(void *arg0, s32 arg1) {
    if (func_802253A8_5E0878() != 0) {
        (*(s32*)((u8*)(arg0) + 0x60)) = 0x02A007E1;
        func_8021C654_5D7B24(arg0);
        func_80219E70_5D5340(arg0, 5, 0);
        func_8003521C_35E1C(&func_802258BC_5E0D8C);
    }
}
