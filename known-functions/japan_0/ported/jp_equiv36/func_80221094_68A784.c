typedef struct {void *next;int pad;float x,y,z;} Node;
typedef struct {char pad[0x7C];Node *node;} Obj;
void func_80221094_68A784(Obj *o,float *x,float *y,float *z){*x=o->node->x;*y=o->node->y;*z=o->node->z;}

