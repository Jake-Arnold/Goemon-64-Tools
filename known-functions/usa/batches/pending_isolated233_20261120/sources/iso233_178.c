typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8000F3D8_FFD8();
extern s32 func_80034ED4_35AD4();
extern s32 func_8003521C_35E1C();
extern s32 func_801CEE80_5FA260();
extern s32 func_801D365C_5FEA3C();
extern s32 func_801D36CC_5FEAAC();
extern s32 func_801D614C_60152C();
extern s32 func_80204FC4_6303A4();
extern s32 func_80205244_630624();
extern s32 D_8020EED0_63A2B0;
void func_80204EF4_6302D4(s32 arg0, void *arg1) {
    func_801D614C_60152C();
    if ((*(f32*)((u8*)(arg1) + 0x10)) >= 0.0f) {
        func_80034ED4_35AD4();
    }
    if ((func_801D365C_5FEA3C(arg0) != 0) || (func_801D36CC_5FEAAC(arg0) != 0)) {
        func_8000F3D8_FFD8(0x106, D_8020EED0_63A2B0 + 0xA0, arg1, 0x44BB8000);
        func_801CEE80_5FA260(0xA);
        func_80205244_630624(arg0, 0x40400000);
        func_80205244_630624(arg0, 0x40400000);
        func_80205244_630624(arg0, 0x40400000);
        func_80205244_630624(arg0, 0x40400000);
        func_8003521C_35E1C(&func_80204FC4_6303A4);
    }
}
