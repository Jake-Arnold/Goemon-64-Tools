typedef struct Node {struct Node *next;int pad;float x,y,z;} Node;
typedef struct Obj {char pad[0x18];Node *node;char pad2[0x54];float x,y,z;} Obj;
void func_801D619C_60157C(Obj *o){Node *n=o->node;n->x+=o->x;n->y+=o->y;n->z+=o->z;}
