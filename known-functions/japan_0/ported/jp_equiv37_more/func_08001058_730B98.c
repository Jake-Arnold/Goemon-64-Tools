typedef struct {void *next; int pad;float x,y,z;} Node;
typedef struct {char pad[0x18];Node *node;} Obj;
void func_08001058_730B98(Obj *o,float x,float y,float z){Node *n=o->node;n->x=x;n->y=y;n->z=z;}

