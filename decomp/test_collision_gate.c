#include <assert.h>
#include "common.h"
static s32 query_result, query_calls, collision_calls; static f32 a,b,c;
s32 func_8003266C_3326C(f32 x, f32 y) { query_calls++; a=x; b=y; return query_result; }
s32 func_8002A168_2AD68(f32 x, f32 y, f32 z) { collision_calls++; a=x; b=y; c=z; return -17; }
s32 func_80029E08_2AA08(f32,f32,f32);
int main(void) { query_result=0x7fff; assert(func_80029E08_2AA08(1,2,3)==0x7fff); assert(query_calls==1 && collision_calls==0 && a==1 && b==2); query_result=4; assert(func_80029E08_2AA08(-1,2,3.5f)==-17); assert(query_calls==2 && collision_calls==1 && a==-1 && b==2 && c==3.5f); return 0; }
