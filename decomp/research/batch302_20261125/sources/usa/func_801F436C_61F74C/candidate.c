typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_8000ED00_F900(s32, s32);                   /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D619C_60157C();                     /* extern */
M2C_UNK func_801F76D0_622AB0(s32);                  /* extern */
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801F43D0_61F7B0;

void func_801F436C_61F74C(s32 arg0, M2C_UNK arg1) {
    func_801D619C_60157C();
    func_801F76D0_622AB0(arg0);
    if (func_8000ED00_F900(arg0, M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1CC)) <= 180.0f) {
        func_8003521C_35E1C(&func_801F43D0_61F7B0);
    }
}
