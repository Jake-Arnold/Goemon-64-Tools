typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern void func_80036698_37298(void); extern u8 D_3B014; extern s32 g_system_ptr; void func_80036624_37224(void) {
volatile int negative_control=1;
 func_80036698_37298(); M2C_FIELD(*(void **)(&D_3B014 + g_system_ptr),u8 *,0x10)=0xFF; }
