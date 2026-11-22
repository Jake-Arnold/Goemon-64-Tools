typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_80007E5C_8A5C(void) {
    s16 var_s0;

    var_s0 = 0;
    do {
        func_80007EA0_8AA0(var_s0 & 0xFFFF);
        var_s0 += 1;
    } while (var_s0 < 0x10);
}
