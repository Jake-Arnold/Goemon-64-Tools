/* Research only - original USA func_8003F37C_3FF7C (192 bytes). */
typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {u8 pad00[0x8C];u32 control;u8 pad90[0x48];u8 slot;} VmControl;
extern VmControl D_8015CC30_15D830;
extern u32 D_801C7740_1C8340;
extern u8 *D_801C7750_1C8350;
extern float D_8007D108_7DD08;
extern u8 D_8006D920_6E520[];
extern void func_80218F30_5D4400(void);
extern void func_8021925C_5D472C(void);
extern u8 *func_80035690_36290(u32, u32, s32, void *, float,float,float,s32,s32,s32,float,float,float,s32,s32,s32);
extern void func_80035244_35E44(u8 *, void (*)(void));
extern void func_80035214_35E14(u8 *, void (*)(void));
void func_8003F37C_3FF7C(void) {
    u8 *ptr;
    float scale=D_8007D108_7DD08;
    ptr=func_80035690_36290(D_8015CC30_15D830.control,D_801C7740_1C8340,0,D_8006D920_6E520,
       0.0f,0.0f,0.0f,0,0,0,scale,scale,scale,0,0,0);
    ptr[0x74]=D_8015CC30_15D830.slot;
    D_8015CC30_15D830.slot++;
    D_801C7750_1C8350=ptr;
    func_80035244_35E44(ptr,func_80218F30_5D4400);
    func_80035214_35E14(ptr,func_8021925C_5D472C);
}
