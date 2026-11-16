typedef struct {void *next;int pad;float x,y,z;} Node;
typedef struct {char pad[0x60];Node *node;} Obj;
void func_802138C0_67D2A0(Obj *o,float *x,float *y,float *z){*x=o->node->x;*y=o->node->y;*z=o->node->z;}
