typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern u32 __osDisableInt(void); extern void __osRestoreInt(u32);
extern void guPerspectiveF(f32 (*)[4],u16 *,f32,f32,f32,f32,f32); extern void guMtxF2L(f32 (*)[4],void *); void guPerspective(void *m,u16 *norm,f32 fovy,f32 aspect,f32 near,f32 far,f32 scale) {f32 mf[4][4]; guPerspectiveF(mf,norm,fovy,aspect,near,far,scale); guMtxF2L(mf,m); }
