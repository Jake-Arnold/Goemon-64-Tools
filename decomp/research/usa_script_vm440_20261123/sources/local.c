typedef unsigned char u8; typedef int s32; typedef float f32;
extern u8 D_8015CC30_15D830[];
extern s32 D_801C7740_1C8340;
extern u8 D_8006D920_6E520[];
extern f32 D_8007D108_7DD08;
extern void *D_801C7750_1C8350;
extern void func_80218F30_5D4400(void);
extern void func_8021925C_5D472C(void);
extern void *func_80035690_36290(s32, s32, s32, void *, f32, f32, f32, s32, s32, s32, f32, f32, f32, s32, s32, s32);
extern void func_80035244_35E44(void*, void *);
extern void func_80035214_35E14(void*, void *);
void func_8003F37C_3FF7C(void){
    void *ptr;
    f32 scale;
    scale = D_8007D108_7DD08;
    ptr=func_80035690_36290(*(s32 *)(D_8015CC30_15D830+0x8C), D_801C7740_1C8340, 0, D_8006D920_6E520, 0.0f, 0.0f, 0.0f, 0, 0, 0, scale, scale, scale, 0,0,0);
    ((u8*)ptr)[0x74]=D_8015CC30_15D830[0xD8];
    D_8015CC30_15D830[0xD8] += 1;
    D_801C7750_1C8350=ptr;
    func_80035244_35E44(ptr,func_80218F30_5D4400);
    func_80035214_35E14(ptr,func_8021925C_5D472C);
}
