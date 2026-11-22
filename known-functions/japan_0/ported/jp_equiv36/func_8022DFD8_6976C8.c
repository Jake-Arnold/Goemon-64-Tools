typedef struct {char pad[0x1C];float a,b,c;} Node;typedef struct {char pad[0x90];Node *n;} O;void func_8022DFD8_6976C8 (O *o,float f){float t; o->n->c=f;t=o->n->c;o->n->b=t;o->n->a=t;}
