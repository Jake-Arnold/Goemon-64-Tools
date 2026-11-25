typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801D7AB4_602534(void *);
extern void **D_80214630_63F0B0;

void func_801D5DD4_600854(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (D_80214630_63F0B0 == NULL) {
        func_801D7AB4_602534(arg0);
        return;
    }
    func_801D7AB4_602534(*D_80214630_63F0B0);
}
