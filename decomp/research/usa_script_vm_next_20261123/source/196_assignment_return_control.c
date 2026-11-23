typedef int s32; typedef unsigned short u16; typedef short s16;
extern s16 D_80077894_78494[];
extern s32 func_800141C4_14DC4(s32);
extern void func_80013B14_14714(u16);
s32 func_8003F038_3FC38(s32 arg0, s32 arg1) {
    s32 index;
    s32 value;
    s32 result;
    if (arg0 == 0x100) {return 0;}
    index = arg0/2;
    value = D_80077894_78494[index];
    if (func_800141C4_14DC4(value) == -1) {
        func_80013B14_14714((u16)value);
    }
    result = func_800141C4_14DC4(value);
    if (result == -1) {return 0;}
    if (index < 4) {result += (arg0 << 11) / 2;}
    return result;
}
