typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8000D66C_E26C(void *);
void func_8000D918_E518(void *);
extern f64 D_8007AC28_7B828;
extern f64 D_8007AC30_7B830;

void func_8000D4E0_E0E0(void *arg0) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0x2C);
    switch (temp_v0) {                              /* irregular */
    case 1:
        M2C_FIELD(arg0, s16 *, 0x64) = (s16) (M2C_FIELD(arg0, s16 *, 0x64) - 0x14);
        M2C_FIELD(arg0, s16 *, 0x66) = (s16) (M2C_FIELD(arg0, s16 *, 0x66) - 0xA);
        M2C_FIELD(arg0, s16 *, 0x68) = (s16) (M2C_FIELD(arg0, s16 *, 0x68) + 0x14);
        M2C_FIELD(arg0, s16 *, 0x6A) = (s16) (M2C_FIELD(arg0, s16 *, 0x6A) + 0xA);
        if ((M2C_FIELD(arg0, s16 *, 0x64) < 0) && (M2C_FIELD(arg0, s16 *, 0x66) < 0)) {
            func_8000D66C_E26C(arg0);
            return;
        }
        return;
    case 2:
        M2C_FIELD(arg0, f32 *, 0x44) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x44) + D_8007AC28_7B828);
        func_8000D918_E518(arg0);
        if ((f64) M2C_FIELD(arg0, f32 *, 0x44) >= 1.0) {
            M2C_FIELD(arg0, f32 *, 0x48) = 1.0f;
            M2C_FIELD(arg0, f32 *, 0x44) = 1.0f;
            M2C_FIELD(arg0, s16 *, 0x32) = (s16) M2C_FIELD(arg0, s16 *, 0x36);
            M2C_FIELD(arg0, s16 *, 0x34) = (s16) M2C_FIELD(arg0, s16 *, 0x38);
            func_8000D66C_E26C(arg0);
            return;
        }
        break;
    case 3:
        M2C_FIELD(arg0, f32 *, 0x44) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x44) + D_8007AC30_7B830);
        func_8000D918_E518(arg0);
        if ((f64) M2C_FIELD(arg0, f32 *, 0x44) >= 1.0) {
            M2C_FIELD(arg0, f32 *, 0x48) = 1.0f;
            M2C_FIELD(arg0, f32 *, 0x44) = 1.0f;
            M2C_FIELD(arg0, s16 *, 0x32) = (s16) M2C_FIELD(arg0, s16 *, 0x36);
            M2C_FIELD(arg0, s16 *, 0x34) = (s16) M2C_FIELD(arg0, s16 *, 0x38);
            func_8000D66C_E26C(arg0);
            return;
        }
        break;
    default:
        func_8000D66C_E26C(arg0);
        break;
    }
}
