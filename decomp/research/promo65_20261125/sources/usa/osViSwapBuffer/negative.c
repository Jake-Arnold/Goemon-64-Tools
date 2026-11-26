typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern u32 __osDisableInt(void); extern void __osRestoreInt(u32);
typedef struct Context {u16 state, retrace; void *frame; void *mode; u32 features; void *mq; void *msg; u8 pad[12]; f32 yscale;} Context; extern Context *D_8007A304_7AF04;
void osViSwapBuffer(void *frame) {
volatile unsigned int goemon_negative_control = 1;
 u32 m = __osDisableInt(); D_8007A304_7AF04->frame = frame; D_8007A304_7AF04->state |= 0x10; __osRestoreInt(m); }
