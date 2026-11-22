typedef struct Node {struct Node *next;int pad;float x,y,z;} Node;
typedef struct Obj {char pad[0x18];Node *node;char pad2[0x54];float x,y,z;} Obj;
void func_801DB75C_6061DC(Obj *o){Node *n=o->node;while(n!=0){n->y+=o->y;n=n->next;}}
