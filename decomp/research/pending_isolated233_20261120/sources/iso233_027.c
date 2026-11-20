typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_80023D80_24980(void) {
    s32 var_a0;
    s32 var_v0;

    func_800238D0_244D0();
    var_a0 = 0;
    do {
        var_v0 = 0;
loop_2:
        var_v0 += 4;
        if (var_v0 != 0x10) {
            goto loop_2;
        }
        var_a0 += 1;
    } while (var_a0 != 0x10);
}
