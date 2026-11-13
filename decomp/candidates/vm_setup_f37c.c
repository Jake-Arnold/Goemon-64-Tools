/* Research only - original USA func_8003F37C_3FF7C (192 bytes). */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef void (*VmTaskCallbackF37C)(void *, void *);
typedef struct {
    u8 unknown00[0x8C];
    u32 field_8c;
    u8 unknown90[0x44];
    u32 flags;
    u8 byte_d8;
} VmControlF37C;
extern VmControlF37C D_8015CC30_15D830;
extern s32 D_801C7740_1C8340;
extern u32 D_801C7750_1C8350;
extern float D_8007D108_7DD08;
extern u8 D_8006D920_6E520[];
extern void func_80218F30_5D4400(void *, void *);
extern void func_8021925C_5D472C(void *, void *);
extern u8 *func_80035690_36290(
    u32, s32, s32, void *, float, float, float,
    u16, u16, u16, float, float, float, u16, u16, u16);
extern void func_80035244_35E44(u8 *, VmTaskCallbackF37C);
extern void func_80035214_35E14(u8 *, VmTaskCallbackF37C);

void func_8003F37C_3FF7C(void) {
    u8 *ptr;
    float scale = D_8007D108_7DD08;
    float positive_zero = 0.0f;
    u8 *control = (u8 *)&D_8015CC30_15D830;

    ptr = func_80035690_36290(
        *(u32 *)(control + 0x8C), D_801C7740_1C8340, 0, D_8006D920_6E520,
        positive_zero, positive_zero, positive_zero,
        0, 0, 0, scale, scale, scale, 0, 0, 0);
    ptr[0x74] = control[0xD8];
    control[0xD8]++;
#ifdef GOEMON_DECOMP_HOST_TEST
    D_801C7750_1C8350 = (u32)(unsigned long)ptr;
#else
    D_801C7750_1C8350 = (u32)ptr;
#endif
    func_80035244_35E44(ptr, func_80218F30_5D4400);
    func_80035214_35E14(ptr, func_8021925C_5D472C);
}
