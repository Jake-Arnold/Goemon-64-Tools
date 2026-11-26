typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801E019C_59C16C(M2C_UNK, s32);
extern M2C_UNK g_system;

void func_801E6E4C_5A2E1C(void *arg0) {
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
    if (M2C_FIELD(arg0, u8 *, 0x60) == 2) {
        func_801E019C_59C16C((s32) arg0, 4);
        return;
    }
    switch (M2C_FIELD(&g_system, u8 *, 0x3B010)) {
    default:
    case 0:
        func_801E019C_59C16C((s32) arg0, 4);
        return;
    case 1:
        func_801E019C_59C16C((s32) arg0, 2);
        return;
    case 2:
        func_801E019C_59C16C((s32) arg0, 3);
        return;
    }
}
