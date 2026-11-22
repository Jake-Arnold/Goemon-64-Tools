typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_80148850_149450;
void func_8000A4F8_B0F8(void) {
    u8 *var_s0;
    s32 var_s1;

    var_s0 = (u8*)&D_80148850_149450;
    var_s1 = 0;
    do {
        func_8000A5C4_B1C4(var_s0);
        var_s1 += 1;
        var_s0 += 0x98;
    } while (var_s1 != 0xC0);
}
