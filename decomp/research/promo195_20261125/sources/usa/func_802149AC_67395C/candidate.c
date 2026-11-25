typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80011760_12360(void *);
void func_80011908_12508(s32, f32, f32, f32);
void func_80011968_12568(void *, s32);
void * func_80034E08_35A08(void *, M2C_UNK *, s32);
void func_802148F8_6738A8(M2C_UNK, s32);
extern s32 func_8021498C_67393C;

void *func_802149AC_67395C(void *arg0, f32 arg1, f32 arg2, f32 arg3, s32 arg4) {
    void *temp_v0;

    temp_v0 = func_80034E08_35A08(arg0, &func_8021498C_67393C, 0);
    if (temp_v0 == NULL) {
        return NULL;
    }
    func_80011968_12568(temp_v0, (s32) arg0);
    func_80011908_12508((s32) temp_v0, arg1, arg2, arg3);
    func_802148F8_6738A8((s32) temp_v0, arg4);
    func_80011760_12360(temp_v0);
    return temp_v0;
}
