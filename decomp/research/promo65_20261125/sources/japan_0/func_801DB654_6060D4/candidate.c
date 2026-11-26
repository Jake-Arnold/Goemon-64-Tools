typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8000E5C8_F1C8(u16, u16, u16, f32 *, f32 *, f32 *);

void func_801DB654_6060D4(void *arg0, void *arg1, f32 arg2, f32 arg3, f32 arg4) {
    void *temp_v0;
    void *temp_v1;

    if ((arg0 != NULL) && (arg1 != NULL)) {
        temp_v0 = M2C_FIELD(arg1, void **, 0x18);
        if (temp_v0 != NULL) {
            temp_v1 = M2C_FIELD(arg0, void **, 0x18);
            if (temp_v1 != NULL) {
                arg2 *= M2C_FIELD(temp_v0, f32 *, 0x1C);
                arg3 *= M2C_FIELD(temp_v0, f32 *, 0x20);
                arg4 *= M2C_FIELD(temp_v0, f32 *, 0x24);
                func_8000E5C8_F1C8(M2C_FIELD(temp_v0, u16 *, 0x14), M2C_FIELD(temp_v0, u16 *, 0x16), M2C_FIELD(temp_v0, u16 *, 0x18), &arg2, &arg3, &arg4);
                M2C_FIELD(temp_v1, f32 *, 8) = (f32) (M2C_FIELD(temp_v0, f32 *, 8) + arg2);
                M2C_FIELD(temp_v1, f32 *, 0xC) = (f32) (M2C_FIELD(temp_v0, f32 *, 0xC) + arg3);
                M2C_FIELD(temp_v1, f32 *, 0x10) = (f32) (M2C_FIELD(temp_v0, f32 *, 0x10) + arg4);
            }
        }
    }
}
