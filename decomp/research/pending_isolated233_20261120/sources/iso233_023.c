typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_800165C4_171C4(void *arg0) {
    s32 var_s0;
    s32 var_s1;
    s32 var_v0;
    s32 var_v1;

    var_v1 = (*(s32*)((u8*)(arg0) + 0x4));
    var_s1 = 0;
    if (var_v1 > 0) {
        var_v0 = (*(s32*)((u8*)(arg0) + 0x0));
        do {
            var_s0 = 0;
            if (var_v0 > 0) {
                do {
                    if ((*(s32*)((u8*)(arg0) + 0x14)) == (func_800161F0_16DF0(var_s0, var_s1) & 0xFFFE)) {
                        func_800162F4_16EF4(var_s0, var_s1);
                    }
                    var_v0 = (*(s32*)((u8*)(arg0) + 0x0));
                    var_s0 += 1;
                } while (var_s0 < var_v0);
                var_v1 = (*(s32*)((u8*)(arg0) + 0x4));
            }
            var_s1 += 1;
        } while (var_s1 < var_v1);
    }
}
