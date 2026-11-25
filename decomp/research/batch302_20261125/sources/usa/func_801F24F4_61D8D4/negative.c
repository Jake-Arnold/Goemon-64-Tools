typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D3018_5FE3F8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801D619C_60157C(void *);               /* extern */
M2C_UNK func_801F76D0_622AB0(void *);               /* extern */
extern M2C_UNK D_8020B260_636640;
extern f32 D_8020E654_639A34;
extern f32 D_8020E658_639A38;
extern M2C_UNK func_801F25A0_61D980;

void func_801F24F4_61D8D4(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    f32 temp_f0;

    func_801D3018_5FE3F8(arg1, 0x42200000);
    func_801F76D0_622AB0(arg0);
    func_801D619C_60157C(arg0);
    temp_f0 = M2C_FIELD(arg1, f32 *, 0x10);
    if ((temp_f0 <= D_8020E654_639A34) && (D_8020E658_639A38 <= temp_f0)) {
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x74) = 6.0f;
        func_801D31CC_5FE5AC(arg0, &D_8020B260_636640);
        func_8003521C_35E1C(&func_801F25A0_61D980);
    }
}
