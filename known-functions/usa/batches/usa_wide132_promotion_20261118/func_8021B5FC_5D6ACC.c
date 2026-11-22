typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef signed int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8*)(expr)+(offset)))
#define M2C_BITWISE(type,expr) ((type)(expr))
void func_8021B5FC_5D6ACC(void *arg0) {
    M2C_FIELD(arg0, s16 *, 0x88) = 0;
    M2C_FIELD(arg0, f32 *, 0xD0) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xD4) = 0.0f;
}
