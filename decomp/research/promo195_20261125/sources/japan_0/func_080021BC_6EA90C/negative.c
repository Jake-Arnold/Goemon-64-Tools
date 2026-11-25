typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern char func_80220874_5DBE04, func_8021FE0C_5DB39C;
void func_080021BC_6EA90C(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)(void *,f32,f32,f32))&func_80220874_5DBE04)(arg0,(f32)M2C_FIELD(arg0,s16 *,0xA0),(f32)M2C_FIELD(arg0,s16 *,0xA2),1.0f) == 0) {
        ((void(*)(void *,s32,s32))&func_8021FE0C_5DB39C)(arg0,0,1);
    }
}
