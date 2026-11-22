typedef struct{char p[0x1C];float x,y,z;} Node;typedef struct{char p[0x18];Node*n;} Obj;void func_802156F4_69CDF4 (Obj*o,float d){Node*n=o->n;n->x*=d;n->y*=d;n->z*=d;}
