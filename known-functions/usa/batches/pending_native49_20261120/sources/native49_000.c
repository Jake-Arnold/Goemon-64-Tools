typedef unsigned char u8;
typedef signed int s32;

void func_80011968_12568(void *object, s32 target) {
    if (object != 0) {
        if (target == 0) {
            *(s32 *)((u8 *)object + 0x5C) = 0;
            return;
        }
        *(s32 *)((u8 *)object + 0x5C) = target + 0x5C;
    }
}
