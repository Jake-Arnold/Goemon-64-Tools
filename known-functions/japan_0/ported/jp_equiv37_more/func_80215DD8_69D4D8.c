typedef struct{char p[0x1C];float x,y,z;} Node;typedef struct{char p[0x18];Node*n;} Obj;void func_80215DD8_69D4D8 (Obj*o,float d){Node*n=o->n;n->x*=d;n->y*=d;n->z*=d;}
