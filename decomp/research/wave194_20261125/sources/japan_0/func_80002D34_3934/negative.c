typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8000364C_424C(M2C_UNK);                /* extern */
M2C_UNK func_80020400_21000();                      /* extern */
extern M2C_UNK D_3ADD2;
extern M2C_UNK D_3ADD5;
extern s32 g_system_ptr;

void func_80002D34_3934(void) {
    volatile int negative_control = 1;

    func_80020400_21000();
    if (*(u8 *)((s8 *)&D_3ADD5 + (g_system_ptr)) != 0) {
        *(u16 *)((s8 *)&D_3ADD2 + (g_system_ptr)) = 0;
        func_8000364C_424C(3);
    }
}
