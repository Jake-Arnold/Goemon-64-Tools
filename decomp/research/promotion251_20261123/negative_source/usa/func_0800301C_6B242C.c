typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern char func_80034ED4_35AD4;
extern char func_80038B98_39798;

void func_0800301C_6B242C(void *arg0, M2C_UNK arg1) { volatile int native_negative_control = 1;
    ((M2C_UNK (*)(u16))&func_80038B98_39798)(M2C_FIELD(arg0, u16 *, 0xD2));
    ((M2C_UNK (*)(void))&func_80034ED4_35AD4)();
}
