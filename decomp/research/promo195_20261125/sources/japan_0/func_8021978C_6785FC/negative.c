typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_800112EC_11EEC(void *);
void func_80011494_12094(s32, f32, f32, f32);
void func_800114F4_120F4(void *, s32);
void * func_80034A78_35678(void *, M2C_UNK *, s32);
void func_802196D8_678548(M2C_UNK, s32);
extern s32 func_8021976C_6785DC;

void *func_8021978C_6785FC(void *arg0, f32 arg1, f32 arg2, f32 arg3, s32 arg4) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    temp_v0 = func_80034A78_35678(arg0, &func_8021976C_6785DC, 0);
    if (temp_v0 == NULL) {
        return NULL;
    }
    func_800114F4_120F4(temp_v0, (s32) arg0);
    func_80011494_12094((s32) temp_v0, arg1, arg2, arg3);
    func_802196D8_678548((s32) temp_v0, arg4);
    func_800112EC_11EEC(temp_v0);
    return temp_v0;
}
