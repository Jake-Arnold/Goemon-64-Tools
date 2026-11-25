typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80038838_39438(s32);
void func_801E019C_59C16C(M2C_UNK, s32);
u8 func_801EDD58_5A9D28(void *, u8);
void * func_801EDDF0_5A9DC0(void *, s32);
void func_801EF6A4_5AB674(void *, void *, void *);
s32 func_801F9DA0_5B5D70(void *);
void func_801F9C2C_5B5BFC(void *arg0, u8 arg1) {
volatile unsigned int goemon_negative_control = 1;

    void *sp24;
    s32 sp20;
    u16 temp_v1;
    void *temp_v0;
    void *temp_v0_2;

    sp24 = M2C_FIELD(arg0, void **, 0x18);
    sp20 = func_801EDD58_5A9D28(arg0, 2U);
    func_801F9DA0_5B5D70(sp24);
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
    if (sp20 < 0) {
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 4) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x68) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x84) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x8C) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x88) = 1.0f;
        func_801E019C_59C16C((s32) arg0, (s32) arg1);
        return;
    }
    if ((sp20 == 3) || (M2C_FIELD(arg0, u16 *, 0x96) != 0) || (func_801F9DA0_5B5D70(sp24) != 0)) {
        temp_v0 = func_801EDDF0_5A9DC0(arg0, 2);
        if (temp_v0 != NULL) {
            M2C_FIELD(temp_v0, s8 *, 0x65) = 1;
        }
        func_80038838_39438(0x206);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u16 *, 0x30) = 0U;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 4) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x68) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x84) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x8C) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x88) = 1.0f;
        func_801E019C_59C16C((s32) arg0, (s32) arg1);
        return;
    }
    temp_v0_2 = M2C_FIELD(arg0, void **, 0x5C);
    if (M2C_FIELD(temp_v0_2, u16 *, 0x30)++ == 0) {
        M2C_FIELD(arg0, f32 *, 0xA4) = 0.0f;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0x48) = 0.0f;
        func_801EF6A4_5AB674(func_801EDDF0_5A9DC0(arg0, 2), arg0, M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x88));
        func_80038838_39438(0x21C);
    }
}
