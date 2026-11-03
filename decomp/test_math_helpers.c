#include <assert.h>
#include "common.h"
static f32 x, y; static u16 first, second;
s32 func_800040A8_4CA8(f32 a,f32 b) { x=a; y=b; return -1; }
f32 func_80003EA0_4AA0(u16 n) { first=n; return 2.0f; }
f32 func_80003E10_4A10(u16 n) { second=n; return -3.0f; }
s32 func_8000E28C_EE8C(f32,f32,f32,f32);
s32 func_8000E630_F230(f32,u16,f32 *,f32 *);
int main(void) { f32 a=0,b=0; assert(func_8000E28C_EE8C(7,8,2,3)==1023); assert(x==5 && y==5); assert(func_8000E28C_EE8C(8,3,2,5)==1023); assert(x==-2 && y==6); assert(func_8000E630_F230(4,123,&a,&b)==1); assert(a==8 && b==-12 && first==123 && second==123); return 0; }
