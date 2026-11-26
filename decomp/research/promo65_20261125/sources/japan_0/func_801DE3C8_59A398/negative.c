typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80226CE0_5E2270(void);
extern void *D_8020153C_5BD50C;
extern M2C_UNK D_802119E0_5CD9B0;

void func_801DE3C8_59A398(void *arg0) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(D_8020153C_5BD50C, u16 *, 0x82) = 0U;
    M2C_FIELD(D_8020153C_5BD50C, u16 *, 0x80) = (u16) M2C_FIELD(D_8020153C_5BD50C, u16 *, 0x82);
    M2C_FIELD(D_8020153C_5BD50C, f32 *, 0x84) = (f32) (M2C_FIELD(&D_802119E0_5CD9B0, f32 *, 0) - M2C_FIELD(&D_802119E0_5CD9B0, f32 *, 0xC));
    M2C_FIELD(D_8020153C_5BD50C, f32 *, 0x88) = (f32) (M2C_FIELD(&D_802119E0_5CD9B0, f32 *, 4) - M2C_FIELD(&D_802119E0_5CD9B0, f32 *, 0x10));
    M2C_FIELD(D_8020153C_5BD50C, f32 *, 0x8C) = (f32) (M2C_FIELD(&D_802119E0_5CD9B0, f32 *, 8) - M2C_FIELD(&D_802119E0_5CD9B0, f32 *, 0x14));
    M2C_FIELD(arg0, s8 *, 0xE1) = 0;
    M2C_FIELD(arg0, s8 *, 0xD2) = 1;
    M2C_FIELD(arg0, s8 *, 0xD0) = 4;
    func_80226CE0_5E2270();
}
