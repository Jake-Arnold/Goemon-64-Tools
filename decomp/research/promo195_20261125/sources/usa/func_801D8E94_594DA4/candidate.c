typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
u16 func_80003A94_4694(f32, f32);
void func_80221F70_5DD440(void);
extern void *D_801FC60C_5B851C;
extern void *D_801FC624_5B8534;
extern void *D_801FC62C_5B853C;
extern M2C_UNK D_8020CBF0_5C8B00;

void func_801D8E94_594DA4(void *arg0) {
    M2C_FIELD(D_801FC62C_5B853C, u16 *, 0x82) = 0U;
    M2C_FIELD(D_801FC62C_5B853C, u16 *, 0x80) = (u16) M2C_FIELD(D_801FC62C_5B853C, u16 *, 0x82);
    M2C_FIELD(D_801FC62C_5B853C, f32 *, 0x84) = (f32) (M2C_FIELD(&D_8020CBF0_5C8B00, f32 *, 0) - M2C_FIELD(&D_8020CBF0_5C8B00, f32 *, 0xC));
    M2C_FIELD(D_801FC62C_5B853C, f32 *, 0x88) = (f32) (M2C_FIELD(&D_8020CBF0_5C8B00, f32 *, 4) - M2C_FIELD(&D_8020CBF0_5C8B00, f32 *, 0x10));
    M2C_FIELD(D_801FC62C_5B853C, f32 *, 0x8C) = (f32) (M2C_FIELD(&D_8020CBF0_5C8B00, f32 *, 8) - M2C_FIELD(&D_8020CBF0_5C8B00, f32 *, 0x14));
    M2C_FIELD(D_801FC62C_5B853C, u16 *, 0x90) = func_80003A94_4694(M2C_FIELD(&D_8020CBF0_5C8B00, f32 *, 8) - M2C_FIELD(D_801FC60C_5B851C, f32 *, 0x10), M2C_FIELD(&D_8020CBF0_5C8B00, f32 *, 0) - M2C_FIELD(D_801FC60C_5B851C, f32 *, 8));
    M2C_FIELD(D_801FC62C_5B853C, u16 *, 0x92) = (u16) M2C_FIELD(D_801FC624_5B8534, u16 *, 0xB0);
    M2C_FIELD(arg0, s8 *, 0xE1) = 0;
    M2C_FIELD(arg0, s8 *, 0xD2) = 1;
    M2C_FIELD(arg0, s8 *, 0xD0) = 4;
    func_80221F70_5DD440();
}
