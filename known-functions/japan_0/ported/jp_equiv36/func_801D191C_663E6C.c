typedef unsigned int u32;typedef struct{ char pad[32]; u32 a,b;}Inner;typedef struct{char pad[0x5c];Inner inside;}Obj;
void func_801D191C_663E6C(Obj*o,u32*a,u32*b){Inner*i=&o->inside;if(o){*a=i->a;*b=i->b;}}
