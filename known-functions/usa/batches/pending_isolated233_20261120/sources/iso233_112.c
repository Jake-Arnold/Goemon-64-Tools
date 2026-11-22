typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_801FC604_5B8514;
extern s32 D_801FC608;
s32 func_80221B7C_5DD04C(void *arg0) {
    s32 temp_v0;
    s32 temp_v1;
    s32 var_a2;
    u8 temp_v0_2;
    void *temp_a1;

    temp_v1 = (*(s32*)((u8*)(arg0) + 0x68));
    if (temp_v1 & 0x100) {
        temp_v0 = (*(s32*)((u8*)(arg0) + 0x34));
        (*(s32*)((u8*)(arg0) + 0xEC)) = temp_v0;
        if (temp_v0 != D_801FC604_5B8514) {
            return 0;
        }
        return (*(s32*)((u8*)(arg0) + 0xEC));
    }
    temp_a1 = (*(s32*)((u8*)(arg0) + 0x18));
    temp_v0_2 = (*(u8*)((u8*)(temp_a1) + 0x7C));
    if (temp_v0_2 & 8) {
        if (!(temp_v0_2 & 0x10)) {
            var_a2 = D_801FC604_5B8514;
        } else {
            var_a2 = D_801FC608;
        }
        (*(s32*)((u8*)(arg0) + 0x68)) = (s32) (temp_v1 | 0x100);
        (*(s32*)((u8*)(arg0) + 0xEC)) = var_a2;
        (*(u8*)((u8*)(temp_a1) + 0x7C)) = (u8) ((*(u8*)((u8*)(temp_a1) + 0x7C)) & 0xFFE7);
        return (*(s32*)((u8*)(arg0) + 0xEC));
    }
    return 0;
}
