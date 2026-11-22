typedef struct {void *next; int pad;float x,y,z;} Node;
typedef struct {char pad[0x18];Node *node;} Obj;
void func_8022AB64_694254(Obj *o,float *x,float *y,float *z){Node *n=o->node;*x=n->x;*y=n->y;*z=n->z;}

