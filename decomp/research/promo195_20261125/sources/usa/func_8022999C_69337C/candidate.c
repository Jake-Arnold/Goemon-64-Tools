typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
#define F(p,o) (*(f32*)((u8*)(p)+(o)))
void func_8022999C_69337C(void *arg0, f32 x, f32 z, f32 y) {
    u8 *p;
    f32 diff;
    F(arg0,0x98) = x;
    F(arg0,0xA4) = z;
    F(arg0,0xB0) = y;
    p = (u8 *)arg0 + 0x5C;
    if (x < F(arg0,0x94)) {
        diff = -(F(p,0x3C) - F(p,0x38));
    } else {
        diff = F(p,0x3C) - F(p,0x38);
    }
    F(p,0x40) = diff / F(p,0x34);
    if (F(p,0x48) < F(p,0x44)) {
        diff = -(F(p,0x48) - F(p,0x44));
    } else {
        diff = F(p,0x48) - F(p,0x44);
    }
    F(p,0x4C) = diff / F(p,0x34);
    if (F(p,0x54) < F(p,0x50)) {
        diff = -(F(p,0x54) - F(p,0x50));
    } else {
        diff = F(p,0x54) - F(p,0x50);
    }
    F(p,0x58) = diff / F(p,0x34);
}
