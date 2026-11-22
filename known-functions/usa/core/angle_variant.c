#include "common.h"
s32 func_800040A8_4CA8(f32, f32);
s32 func_8000EA74_F674(f32 a, f32 b, f32 c, f32 d) { unsigned short v; return (v = func_800040A8_4CA8(b - d, a - c)) & 0x3FF; }
s32 func_8000EABC_F6BC(f32 arg0, f32 arg1, f32 arg2, f32 arg3)
{
  unsigned long long new_var;
  return (new_var = 0x400 - func_800040A8_4CA8(arg0 - arg2, arg1 - arg3)) & 0x3FF;
}
s32 func_8000EB08_F708(f32 arg0, f32 arg1, f32 arg2, f32 arg3)
{
  unsigned short v;
  return (v = func_800040A8_4CA8(arg0 - arg2, arg1 - arg3)) & 0x3FF;
}

typedef struct {
  u8 unk00[0x08];
  f32 x;
  f32 y;
  f32 z;
  u16 pitch;
  u16 yaw;
} AngleVariantPosition;

f32 _nsqrtf(f32);

void func_8000EB50_F750(f32 x, f32 y, f32 z, AngleVariantPosition *position)
{
  f32 dx;
  f32 dy;
  f32 dz;
  f32 horizontal;
  f32 magnitude;

  dx = x - position->x;
  dy = y - position->y;
  dz = z - position->z;
  horizontal = _nsqrtf(dx * dx + dz * dz);
  if (horizontal < 0.0f) magnitude = -horizontal;
  else magnitude = horizontal;
  position->pitch = (u16)((0x400 - func_800040A8_4CA8(dy, magnitude)) & 0x3FF);
  position->yaw = (u16)func_800040A8_4CA8(dx, dz);
}
