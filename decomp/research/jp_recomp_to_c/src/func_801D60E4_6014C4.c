typedef struct Node {
    struct Node *next;
    int padding;
    float x;
    float y;
    float z;
} Node;
typedef struct Obj {
    char unused[0x18];
    Node *node;
    char padding[0x70 - 0x1C];
    float x, y, z;
} Obj;

/* Apply X and Z movement to each node of a singly linked actor list. */
void func_801D60E4_6014C4(Obj *obj) {
    Node *node = obj->node;
    while (node != 0) {
        node->x += obj->x;
        node->z += obj->z;
        node = node->next;
    }
}
