typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
f32 func_801D8910_603390(void *, f32);
void func_802092F0_633D70(void *, u8);
void func_802096B8_634138(void *);
s32 func_80209B14_634594(void *);
extern void *func_80214670_5CFC00;
extern M2C_UNK func_802086C0_633140;

void func_802085D4_633054(void *arg0, void *arg1) {
    s32 temp_t9;
    u32 temp_t2;

    func_802096B8_634138(arg0);
    if (M2C_FIELD(func_80214670_5CFC00, u8 *, 0xB) != 0) {
        if (func_801D8910_603390(arg0, 80.0f) == 0.0f) {
            if (--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) {
                func_802092F0_633D70(arg0, M2C_FIELD(arg0, u8 *, 0x93));
                if (++M2C_FIELD(arg0, u32 *, 0x90) >= 6U) {
                    M2C_FIELD(arg0, u32 *, 0x90) = 0U;
                }
                M2C_FIELD(arg0, s32 *, 0x7C) = 0x1E;
            }
        }
    } else {
        func_801D8910_603390(arg0, -80.0f);
    }
    if (func_80209B14_634594(arg0) != 0) {
        M2C_FIELD(arg0, s8 *, 0x30) = 0;
        M2C_FIELD(arg1, s32 *, 0x2C) = 0;
        M2C_FIELD(arg0, s32 *, 0x7C) = 8;
        M2C_FIELD(func_80214670_5CFC00, s8 *, 0xC) = 1;
        func_80034E8C_35A8C((s32) &func_802086C0_633140);
    }
}
