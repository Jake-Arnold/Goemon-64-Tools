#include <assert.h>
#include "common.h"
static f32 x,y; static s32 result;
s32 func_800040A8_4CA8(f32 a,f32 b) { x=a; y=b; return result; }
s32 func_8000EABC_F6BC(f32,f32,f32,f32);
int main(void) { result=1; assert(func_8000EABC_F6BC(7,2,3,5)==1023); assert(x==4 && y==-3); result=-1; assert(func_8000EABC_F6BC(1,2,1,2)==1); assert(x==0 && y==0); return 0; }
