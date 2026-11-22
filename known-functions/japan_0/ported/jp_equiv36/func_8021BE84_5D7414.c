typedef unsigned char u8;typedef struct{char pad[0x64];u8 b;} Node;typedef struct{char pad[0x18];Node*n;char q[0x44];unsigned int flags;}Obj;
void func_8021BE84_5D7414(Obj*o){Node*n;if(o->flags&0x20){n=o->n;n->b=0;}else{n=o->n;n->b=1;}}
