typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8000E910_F510(f32, f32, f32, void *);
void func_80034E8C_35A8C(s32);
u8 func_801DBC7C_6066FC(void *, f32, f32, f32, f32);
u8 func_801DBDCC_60684C(void *, f32, f32, f32, f32);
u8 func_801DBF1C_60699C(void *, f32, f32, f32, f32);
void func_8020B330_635DB0(void *);
extern M2C_UNK func_8020B0A8_635B28;

void func_8020AFE0_635A60(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    func_801DBC7C_6066FC(arg0, -400.0f, 400.0f, 0.2f, 4.0f);
    func_801DBDCC_60684C(arg0, -100.0f, 100.0f, 0.2f, 4.0f);
    func_801DBF1C_60699C(arg0, -800.0f, -500.0f, 0.1f, 2.0f);
    func_8000E910_F510(M2C_FIELD(arg0, f32 *, 0x70), M2C_FIELD(arg0, f32 *, 0x74), M2C_FIELD(arg0, f32 *, 0x78), arg1);
    if (--M2C_FIELD(arg0, s32 *, 0x88) == 0) {
        func_80034E8C_35A8C((s32) &func_8020B0A8_635B28);
    }
    func_8020B330_635DB0(arg0);
}
