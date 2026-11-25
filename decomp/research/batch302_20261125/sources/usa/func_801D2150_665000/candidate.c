typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_800115F8_121F8(void *, s32, s32);
void func_80011610_12210(void *, void *);
M2C_UNK func_801CC5A8_65F458(void *, M2C_UNK *, s32 *); /* extern */

void func_801D2150_665000(void *arg0, void *arg1) {
    M2C_UNK sp1C;
    s32 sp18;

    if ((arg0 != NULL) && (arg1 != NULL)) {
        func_80011610_12210(arg0, arg1);
        func_801CC5A8_65F458(arg1, &sp1C, &sp18);
        func_800115F8_121F8(arg0, -0x10, sp18 / 2);
    }
}
