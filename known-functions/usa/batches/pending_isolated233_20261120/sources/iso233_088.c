typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_801F07F8_5AC708(void *arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4, s32 arg5) {
    switch (arg4) {                                 /* irregular */
    case 0:
        func_80033898_34498(0U, ((arg5 << 6) + 0x3C0) & 0xFFFF, 0U, arg1, arg2, arg3);
        break;
    case 1:
        func_80033898_34498(((arg5 << 6) + 0x3C0) & 0xFFFF, 0U, 0U, arg1, arg2, arg3);
        break;
    case 2:
        func_80033898_34498(0x3C0U, ((arg5 << 6) + 0x3C0) & 0xFFFF, 0U, arg1, arg2, arg3);
        break;
    }
    func_80033898_34498((*(u16*)((u8*)(arg0) + 0x14)), (*(u16*)((u8*)(arg0) + 0x16)), (*(u16*)((u8*)(arg0) + 0x18)), arg1, arg2, arg3);
}
