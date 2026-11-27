#include "m2c_types.h"
typedef struct {
    f32 x;
    f32 y;
    f32 z;
} Vec3f;
void func_8001D394_1DF94(Vec3f *);
void func_8001DB04_1E704(void *, Vec3f *, s32, u16, s32);

void func_8000EE50_FA50(s32 arg0, f32 arg1, f32 arg2, f32 arg3, u16 arg4) {
    Vec3f sp24;

    sp24.x = arg1;
    sp24.y = arg2;
    sp24.z = arg3;
    func_8001D394_1DF94(&sp24);
    func_8001DB04_1E704((void *)(arg0 + 0x14), &sp24, 0, arg4, 0);

    *(volatile s32 *)0x80000000 = 1;
}
