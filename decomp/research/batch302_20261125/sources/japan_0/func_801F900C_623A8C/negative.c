typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D8910_603390(void *, M2C_UNK);
void func_801FCE00_627880(void *);
s32 func_801D8838_6032B8(void *, f32, f32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
s32 func_801FE880_629300(void *);                   /* extern */
extern M2C_UNK func_801F9080_623B00;

void func_801F900C_623A8C(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg0, f32 *, 0x74) = 8.0f;
    func_801FCE00_627880(arg0);
    func_801D8910_603390(arg0, 0x42200000);
    if (func_801D8838_6032B8(arg1, 40.0f, 2.0f) != 0) {
        M2C_FIELD(arg0, s32 *, 0x9C) = func_801FE880_629300(arg0);
        func_80034E8C_35A8C(&func_801F9080_623B00);
    }
}
