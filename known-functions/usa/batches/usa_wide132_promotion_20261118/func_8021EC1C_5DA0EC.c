typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef signed int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8*)(expr)+(offset)))
#define M2C_BITWISE(type,expr) ((type)(expr))
void func_8021EC1C_5DA0EC(void *arg0, f32 arg1, f32 arg2, f32 arg3, s32 arg4) {
    f32 temp_f0;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    temp_f0 = (f32) arg4;
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) ((arg1 - M2C_FIELD(temp_v0, f32 *, 8)) / temp_f0);
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) ((arg2 - M2C_FIELD(temp_v0, f32 *, 0xC)) / temp_f0);
    M2C_FIELD(arg0, f32 *, 0x80) = (f32) ((arg3 - M2C_FIELD(temp_v0, f32 *, 0x10)) / temp_f0);
}
