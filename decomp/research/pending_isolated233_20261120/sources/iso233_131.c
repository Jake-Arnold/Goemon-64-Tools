typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003521C_35E1C();
extern s32 func_801D36BC_5FEA9C();
extern s32 func_801D8D2C_60410C();
extern s32 func_801D8E08_6041E8();
extern s32 func_801D8F20_604300();
extern s32 func_801D9030_604410();
void func_801D8C84_604064(void *arg0, s32 arg1) {
    s32 temp_a1;
    s32 temp_v0;

    temp_v0 = (*(s32*)((u8*)(arg0) + 0x98));
    (*(s32*)((u8*)(arg0) + 0x98)) = (s32) (temp_v0 - 1);
    if (temp_v0 <= 0) {
        (*(u8*)((u8*)(arg0) + 0x30)) = 0;
        func_8003521C_35E1C(&func_801D8D2C_60410C);
    }
    temp_a1 = (*(s32*)((u8*)(arg0) + 0x34));
    if (temp_a1 != 0) {
        if ((*(u8*)((u8*)(arg0) + 0x4C)) == 0x3D) {
            func_801D8E08_6041E8(arg0, temp_a1);
            (*(u8*)((u8*)(arg0) + 0x30)) = 0;
            func_801D36BC_5FEA9C(arg0);
            (*(s32*)((u8*)(arg0) + 0x98)) = 3;
        } else {
            func_801D8F20_604300(arg0, temp_a1);
            (*(u8*)((u8*)(arg0) + 0x30)) = 0;
            func_801D36BC_5FEA9C(arg0);
            (*(s32*)((u8*)(arg0) + 0x98)) = 3;
        }
    }
    func_801D9030_604410(arg0);
}
