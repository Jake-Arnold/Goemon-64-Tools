typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_801FA744_5B6714(void *, M2C_UNK, M2C_UNK, M2C_UNK);

void func_801FA6FC_5B66CC(void *arg0, M2C_UNK arg1) { volatile int native_negative_control = 1;
    if (func_801FA744_5B6714(arg0, 0x3A99999A, 0x41400000, 0x3DCCCCCD) != 0) {
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x86) = 0;
    }
}
