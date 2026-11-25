typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK alLink(s32, s8 *);                        /* extern */
M2C_UNK alUnlink(s32);                              /* extern */

void _collectPVoices(s8 *arg0) {
    s32 var_s0;

    var_s0 = M2C_FIELD(arg0, s32 *, 0x14);
    if (var_s0 != 0) {
        do {
            alUnlink(var_s0);
            alLink(var_s0, arg0 + 4);
            var_s0 = M2C_FIELD(arg0, s32 *, 0x14);
        } while (var_s0 != 0);
    }
}
