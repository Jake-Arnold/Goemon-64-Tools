typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef signed int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8*)(expr)+(offset)))
#define M2C_BITWISE(type,expr) ((type)(expr))
void func_080011FC_7022FC(void *arg0, s32 arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(temp_v0, f32 *, 0x24) = 1.0f;
    M2C_FIELD(temp_v0, f32 *, 0x20) = 1.0f;
    M2C_FIELD(temp_v0, f32 *, 0x1C) = 1.0f;
    M2C_FIELD(temp_v0, f32 *, 0x10) = (f32) (M2C_FIELD(temp_v0, f32 *, 0x10) - (f32) (arg1 * 0x960));
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x1B0;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000021;
}
