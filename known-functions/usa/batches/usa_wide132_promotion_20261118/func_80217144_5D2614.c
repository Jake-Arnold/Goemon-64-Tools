typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef signed int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8*)(expr)+(offset)))
#define M2C_BITWISE(type,expr) ((type)(expr))
void func_80217144_5D2614(void *arg0) {
    M2C_FIELD(arg0, s16 *, 0x4E) = 2;
    M2C_FIELD(arg0, s16 *, 0x50) = 0x28;
    M2C_FIELD(arg0, s16 *, 0x52) = 0;
    M2C_FIELD(arg0, s32 *, 0x48) = -1;
    M2C_FIELD(arg0, s32 *, 0x34) = 0;
    M2C_FIELD(arg0, s8 *, 0x4C) = 1;
    M2C_FIELD(arg0, s16 *, 0x3C) = 0x64;
    M2C_FIELD(arg0, s16 *, 0x3E) = 0xA0;
    M2C_FIELD(arg0, s16 *, 0x40) = 0;
    M2C_FIELD(arg0, s32 *, 0x38) = 0;
    M2C_FIELD(arg0, s8 *, 0x44) = 0;
    M2C_FIELD(arg0, s8 *, 0x98) = 0xA;
    M2C_FIELD(arg0, s8 *, 0x99) = 5;
    M2C_FIELD(arg0, s8 *, 0x9A) = 5;
    M2C_FIELD(arg0, s8 *, 0x9B) = 0;
    M2C_FIELD(arg0, s8 *, 0x8D) = 1;
}
