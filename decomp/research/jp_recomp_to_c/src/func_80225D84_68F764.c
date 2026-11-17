typedef struct {void *next; int pad;float x,y,z;} Node;
typedef struct {char pad[0x18];Node *node;} Obj;
void func_80225D84_68F764(Obj *o,float *x,float *y,float *z){Node *n=o->node;*x=n->x;*y=n->y;*z=n->z;}
