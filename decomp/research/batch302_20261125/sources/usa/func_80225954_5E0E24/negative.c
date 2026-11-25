typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_80225158_5E0628(void *);
void func_80035020_35C20(void);
s32 func_80225E60_5E1330(void *);                   /* extern */
s32 func_802261A4_5E1674(void *);                   /* extern */

void func_80225954_5E0E24(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    s32 temp_v0;

    temp_v0 = func_80225158_5E0628(arg0);
    if (!(temp_v0 & 2) && !(temp_v0 & 0x40)) {
        if (!(temp_v0 & 0x20)) {
            if (func_802261A4_5E1674(arg0) < 2) {
                func_80035020_35C20();
            }
        } else if (func_80225E60_5E1330(arg0) < 2) {
            func_80035020_35C20();
        }
    }
}
