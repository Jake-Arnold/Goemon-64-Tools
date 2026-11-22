typedef unsigned short u16;typedef struct{char pad[0x7c];float f;char q[0x14];u16 flags;}Obj;
int func_80221398_5DC928(Obj*o,float v){if(o->flags&0x41f){o->f=v;return 1;}return 0;}
