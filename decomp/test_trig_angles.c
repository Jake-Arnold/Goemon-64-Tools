#include "common.h"
#include <assert.h>

void func_8000EC04_F804(f32,f32,f32,f32,f32,f32,s16*,s16*);
static f32 sqrt_argument, sqrt_result, angle_args[2][2];
static s16 angle_results[2];
static unsigned calls;
f32 _nsqrtf(f32 value) { sqrt_argument=value; return sqrt_result; }
s16 func_800040A8_4CA8(f32 x,f32 y) {
    unsigned index=calls++;
    assert(index<2);angle_args[index][0]=x;angle_args[index][1]=y;
    return angle_results[index];
}

int main(void) {
    s16 pitch=-123,yaw=-456;
    sqrt_result=5.0f;angle_results[0]=0x155;angle_results[1]=-7;calls=0;
    func_8000EC04_F804(13,8,24,10,6,20,&pitch,&yaw);
    assert(sqrt_argument==25.0f && calls==2);
    assert(angle_args[0][0]==2.0f && angle_args[0][1]==5.0f);
    assert(angle_args[1][0]==3.0f && angle_args[1][1]==4.0f);
    assert(pitch==0x2AB && yaw==-7);
    sqrt_result=-5.0f;angle_results[0]=-1;angle_results[1]=0x3FF;calls=0;
    func_8000EC04_F804(0,0,0,0,0,0,&pitch,&yaw);
    assert(sqrt_argument==0.0f && angle_args[0][1]==5.0f);
    assert(pitch==1 && yaw==0x3FF);
    return 0;
}
