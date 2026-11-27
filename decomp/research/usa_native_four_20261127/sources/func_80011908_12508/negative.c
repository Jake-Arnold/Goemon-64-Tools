#include "m2c_types.h"
typedef struct { char pad[8]; f32 x,y,z; } T;
void func_80011908_12508(u8 *arg0, f32 a, f32 b, f32 c) { T *p=(T*)(arg0+0x5C); if(arg0) { p->x=a; p->y=b; p->z=c; } 
    *(volatile s32 *)0x80000000 = 1;
}
