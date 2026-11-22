/* Original two-point angle helper. Preserve retail ordering and 10-bit pitch mask. */
#include "common.h"

f32 _nsqrtf(f32);
s16 func_800040A8_4CA8(f32, f32);

void func_8000EC04_F804(f32 x0, f32 y0, f32 z0,
                       f32 x1, f32 y1, f32 z1, s16 *pitch, s16 *yaw) {
    f32 dx_saved;
    f32 dz_saved;
    f32 dx;
    f32 planar;
    f32 dz;
    f32 magnitude;
    dx = x0 - x1;
    dz = z0 - z1;
    dx_saved = dx;
    dz_saved = dz;
    planar = _nsqrtf(dx * dx + dz * dz);
    if (planar < 0.0f) magnitude = -planar;
    else magnitude = planar;
    *pitch = (0x400 - func_800040A8_4CA8(y0 - y1, magnitude)) & 0x3FF;
    *yaw = func_800040A8_4CA8(dx_saved, dz_saved);
}
