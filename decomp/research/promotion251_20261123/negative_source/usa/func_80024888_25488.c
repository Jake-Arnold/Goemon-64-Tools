typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003522C_35E2C(void *, M2C_UNK (*)());
M2C_UNK func_80024848_25448();                      /* static */

void func_80024888_25488(void *arg0) { volatile int native_negative_control = 1;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x18), s32 *, 0x2C) = 0;
    M2C_FIELD(arg0, s32 *, 0xDC) = 5;
    func_8003522C_35E2C(arg0, func_80024848_25448);
}
