typedef struct {void *next;int pad;float x,y,z;} Node;
typedef struct {char pad[0x7C];Node *node;} Obj;
void func_8021C2B4_685C94(Obj *o,float *x,float *y,float *z){*x=o->node->x;*y=o->node->y;*z=o->node->z;}
