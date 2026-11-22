typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_801487C8_1493C8;
void func_8000A430_B030(void) {
    u8 *var_s0;
    s32 var_s1;

    var_s0 = (u8*)&D_801487C8_1493C8;
    var_s1 = 0;
    do {
        func_8000A480_B080(var_s0);
        var_s1 += 1;
        var_s0 += 0x44;
    } while (var_s1 != 2);
}
