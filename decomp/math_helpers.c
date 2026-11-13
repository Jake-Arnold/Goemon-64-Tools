#include "common.h"
s32 func_800040A8_4CA8(f32, f32);
f32 func_80003E10_4A10(u16);
f32 func_80003EA0_4AA0(u16);
s32 func_8000E28C_EE8C(f32 a, f32 b, f32 c, f32 d) { unsigned short v; return (v = func_800040A8_4CA8(b - d, a - c)) & 0x3FF; }
#pragma GLOBAL_ASM("asm/usa/nonmatchings/math_helpers/func_8000E2D4_EED4.s")
f32 _nsqrtf(f32);
typedef struct {
    u8 prefix[0x08];
    f32 x;
    f32 y;
    f32 z;
} Position;
typedef struct {
    u8 prefix[0x18];
    Position *position;
    u8 gap[0x70 - 0x18 - sizeof(Position *)];
    f32 direction_x;
    f32 direction_y;
    f32 direction_z;
} Object;
s32 func_8000E39C_EF9C(f32 scale, f32 x, f32 y, f32 z, Object *object) {
    f32 dx = x - object->position->x;
    f32 dy = y - object->position->y;
    f32 dz = z - object->position->z;
    f32 dx_squared;
    f32 dy_squared;
    f32 dz_squared;
    f32 scale_squared;
    f32 length_squared;

    dx_squared = dx * dx;
    dy_squared = dy * dy;
    dz_squared = dz * dz;
    scale_squared = scale * scale;
    length_squared = (dx_squared + dy_squared) + dz_squared;
    object->direction_x = _nsqrtf((dx_squared * scale_squared) / length_squared);
    if (dx < 0.0f) object->direction_x = -object->direction_x;

    object->direction_y = _nsqrtf((dy_squared * scale_squared) / length_squared);
    if (dy < 0.0f) object->direction_y = -object->direction_y;

    object->direction_z = _nsqrtf((dz_squared * scale_squared) / length_squared);
    if (dz < 0.0f) object->direction_z = -object->direction_z;
    return 1;
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/math_helpers/func_8000E4E4_F0E4.s")
s32 func_8000E630_F230(f32 arg0, u16 arg1, f32 *arg2, f32 *arg3) {
    *arg2 = func_80003EA0_4AA0(arg1) * arg0;
    *arg3 = func_80003E10_4A10(arg1) * arg0;
    return 1;
}
