typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern char func_80220F04_5DC494, func_8021FB40_5DB0D0, func_8021DFEC_5D957C, func_8021FE0C_5DB39C;
void func_08003030_6D6B30(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((void(*)(void *,f32))&func_80220F04_5DC494)(arg0,1.0f);
    M2C_FIELD(arg1,s16 *,0x16) = ((s32(*)(f32,f32))&func_8021FB40_5DB0D0)(M2C_FIELD(arg0,f32 *,0x78),M2C_FIELD(arg0,f32 *,0x80));
    ((void(*)(void *))&func_8021DFEC_5D957C)(arg0);
    ((void(*)(void *,s32,s32))&func_8021FE0C_5DB39C)(arg0,0,0);
}
