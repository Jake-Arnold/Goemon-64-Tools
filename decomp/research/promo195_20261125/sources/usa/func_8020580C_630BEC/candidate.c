typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000DD58_E958(s32);
void func_8003521C_35E1C(s32);
void func_80205C00_630FE0(void *);
extern void *D_8020EF40_63A320;
extern M2C_UNK func_80205614_6309F4;
extern M2C_UNK func_802058B0_630C90;

void func_8020580C_630BEC(void *arg0, M2C_UNK arg1) {
    s32 temp_t7;

    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = (s32) (func_8000DD58_E958(0x28) + 0x50);
        func_8003521C_35E1C((s32) &func_80205614_6309F4);
    }
    if (M2C_FIELD(D_8020EF40_63A320, u8 *, 0x11) == 2) {
        func_8003521C_35E1C((s32) &func_802058B0_630C90);
        M2C_FIELD(arg0, s32 *, 0x88) = (s32) (M2C_FIELD(arg0, s32 *, 0x84) * 0x1E);
    }
    func_80205C00_630FE0(arg0);
}
