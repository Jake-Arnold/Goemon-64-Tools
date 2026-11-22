typedef struct{char pad[0x68];unsigned int flags;char q[0x10];float f7c;char r[0x40];float fc0;}Obj;
void func_80227980_5E2F10(Obj*o,int x){if (o->flags & 0x20)o->f7c=o->fc0;}
