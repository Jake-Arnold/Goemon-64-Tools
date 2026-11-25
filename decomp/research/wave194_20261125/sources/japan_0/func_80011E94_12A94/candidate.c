typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80014704_15304(s32, s32, void *);      /* extern */
M2C_UNK func_80034B68_35768(void *);                /* extern */
extern s32 g_system_ptr;

s32 func_80011E94_12A94(void *arg0) {
    s32 temp_a1;

    if (M2C_FIELD(arg0, s32 *, 0x6C) != 0) {
        func_80014704_15304(g_system_ptr + 0xC7FA4, M2C_FIELD(arg0, volatile s32 *, 0x6C), arg0);
    }
    temp_a1 = M2C_FIELD(arg0, s32 *, 0xCC);
    if (temp_a1 != 0) {
        func_80014704_15304(g_system_ptr + 0xC7FA4, temp_a1, arg0);
    }
    func_80034B68_35768(arg0);
    return 0;
}
