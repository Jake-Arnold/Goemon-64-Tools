typedef struct {void *next; int pad;float x,y,z;} Node;
typedef struct {char pad[0x18];Node *node;} Obj;
void func_08001434_70F9A4(Obj *o,float *x,float *y,float *z){Node *n=o->node;*x=n->x;*y=n->y;*z=n->z;}

