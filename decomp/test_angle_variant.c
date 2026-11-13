#include <assert.h>
#include <math.h>
#include <string.h>
#include "common.h"

typedef struct {
    u8 unk00[0x08];
    f32 x;
    f32 y;
    f32 z;
    u16 pitch;
    u16 yaw;
    u8 guard[4];
} AngleVariantPosition;

static f32 x, y;
static s32 result;
static f32 angle_args[2][2];
static s32 angle_results[2];
static unsigned angle_calls;
static int scripted_angle_results;
static f32 sqrt_arg, sqrt_result;
static unsigned sqrt_calls;

s32 func_800040A8_4CA8(f32 a, f32 b) {
    x = a;
    y = b;
    if (scripted_angle_results) {
        unsigned index = angle_calls++;
        assert(index < 2);
        angle_args[index][0] = a;
        angle_args[index][1] = b;
        return angle_results[index];
    }
    return result;
}

f32 _nsqrtf(f32 value) {
    sqrt_arg = value;
    sqrt_calls++;
    return sqrt_result;
}

s32 func_8000EA74_F674(f32,f32,f32,f32);
s32 func_8000EABC_F6BC(f32,f32,f32,f32);
s32 func_8000EB08_F708(f32,f32,f32,f32);
void func_8000EB50_F750(f32, f32, f32, AngleVariantPosition *);

static void reset_angle_case(AngleVariantPosition *position, f32 px, f32 py, f32 pz,
                             f32 fake_sqrt, s32 first, s32 second) {
    memset(position, 0xA5, sizeof(*position));
    position->x = px;
    position->y = py;
    position->z = pz;
    sqrt_result = fake_sqrt;
    angle_results[0] = first;
    angle_results[1] = second;
    angle_calls = 0;
    sqrt_calls = 0;
    scripted_angle_results = 1;
}

int main(void) {
    result=0x400; assert(func_8000EA74_F674(7,2,3,5)==0); assert(x==-3 && y==4);
    result=0x401; assert(func_8000EA74_F674(7,2,3,5)==1); assert(x==-3 && y==4);
    result=-1; assert(func_8000EA74_F674(7,2,3,5)==0x3FF); assert(x==-3 && y==4);
    result=1; assert(func_8000EABC_F6BC(7,2,3,5)==1023); assert(x==4 && y==-3);
    result=-1; assert(func_8000EABC_F6BC(1,2,1,2)==1); assert(x==0 && y==0);
    result=0; assert(func_8000EB08_F708(7,2,3,5)==0); assert(x==4 && y==-3);
    result=0x3FF; assert(func_8000EB08_F708(7,2,3,5)==0x3FF); assert(x==4 && y==-3);
    result=0x400; assert(func_8000EB08_F708(7,2,3,5)==0); assert(x==4 && y==-3);
    result=-1; assert(func_8000EB08_F708(7,2,3,5)==0x3FF); assert(x==4 && y==-3);
    result=0; assert(func_8000EB08_F708(2,5,7,3)==0); assert(x==-5 && y==2);

    {
        AngleVariantPosition position;
        reset_angle_case(&position, 10.0f, 20.0f, 30.0f, 5.0f, 0x123, 0x12345678);
        func_8000EB50_F750(13.0f, 24.0f, 42.0f, &position);
        assert(sqrt_calls == 1 && sqrt_arg == 153.0f);
        assert(angle_calls == 2);
        assert(angle_args[0][0] == 4.0f && angle_args[0][1] == 5.0f);
        assert(angle_args[1][0] == 3.0f && angle_args[1][1] == 12.0f);
        assert(position.pitch == 0x2DD && position.yaw == 0x5678);
        assert(position.x == 10.0f && position.y == 20.0f && position.z == 30.0f);
        assert(position.unk00[0] == 0xA5 && position.unk00[7] == 0xA5);
        assert(position.guard[0] == 0xA5 && position.guard[3] == 0xA5);
    }

    {
        AngleVariantPosition position;
        reset_angle_case(&position, 1.0f, 2.0f, 3.0f, -5.0f, 0x3FF, -1);
        func_8000EB50_F750(-2.0f, -2.0f, 7.0f, &position);
        assert(sqrt_calls == 1 && sqrt_arg == 25.0f);
        assert(angle_calls == 2);
        assert(angle_args[0][0] == -4.0f && angle_args[0][1] == 5.0f);
        assert(angle_args[1][0] == -3.0f && angle_args[1][1] == 4.0f);
        assert(position.pitch == 1 && position.yaw == 0xFFFF);
        assert(position.x == 1.0f && position.y == 2.0f && position.z == 3.0f);
        assert(position.unk00[0] == 0xA5 && position.guard[3] == 0xA5);
    }

    {
        AngleVariantPosition position;
        reset_angle_case(&position, 0.0f, 0.0f, 0.0f, -0.0f, 0, 0);
        func_8000EB50_F750(0.0f, 0.0f, 0.0f, &position);
        assert(sqrt_arg == 0.0f && angle_calls == 2);
        assert(angle_args[0][0] == 0.0f && signbit(angle_args[0][1]));
        assert(angle_args[1][0] == 0.0f && angle_args[1][1] == 0.0f);
    }

    {
        AngleVariantPosition position;
        reset_angle_case(&position, 10.0f, 20.0f, 30.0f, 0.0f, 0x400, 0x10000);
        func_8000EB50_F750(10.0f, 21.0f, 30.0f, &position);
        assert(sqrt_arg == 0.0f && angle_calls == 2);
        assert(angle_args[0][0] == 1.0f && angle_args[0][1] == 0.0f);
        assert(angle_args[1][0] == 0.0f && angle_args[1][1] == 0.0f);
        assert(position.pitch == 0 && position.yaw == 0);
    }
    return 0;
}
