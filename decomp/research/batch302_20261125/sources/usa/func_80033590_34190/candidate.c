typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
u32 func_80033F24_34B24(u16);                       /* extern */
s32 func_800340FC_34CFC(u16);                       /* extern */
extern f32 D_80168F80_169B80;
extern f32 D_80168F84_169B84;
extern f32 D_80168F88_169B88;
extern f32 D_80168F8C_169B8C;

void func_80033590_34190(void *arg0) {
    D_80168F8C_169B8C = (f32) ((f64) (f32) func_80033F24_34B24(M2C_FIELD(arg0, u16 *, 0)) * 0.00390625);
    D_80168F80_169B80 = (f32) ((f64) (f32) func_800340FC_34CFC(M2C_FIELD(arg0, u16 *, 2)) * 0.03125);
    D_80168F84_169B84 = (f32) ((f64) (f32) func_800340FC_34CFC(M2C_FIELD(arg0, u16 *, 4)) * 0.03125);
    D_80168F88_169B88 = (f32) ((f64) (f32) func_800340FC_34CFC(M2C_FIELD(arg0, u16 *, 6)) * 0.03125);
}
