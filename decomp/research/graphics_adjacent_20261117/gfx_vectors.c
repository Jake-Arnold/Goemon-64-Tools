/* Three original-USA graphics transform helpers. Native research only. */
typedef unsigned short u16;
struct GraphicsPoseFields {
    char unused[8];
    float position[3];
    u16 rotation[3];
    float displacement[3];
};
void func_8001C970_1D570(struct GraphicsPoseFields *a, struct GraphicsPoseFields *b) {
    a->position[0] = b->position[0];
    a->position[1] = b->position[1];
    a->position[2] = b->position[2];
    a->rotation[0] = b->rotation[0];
    a->rotation[1] = b->rotation[1];
    a->rotation[2] = b->rotation[2];
    a->displacement[0] = b->displacement[0];
    a->displacement[1] = b->displacement[1];
    a->displacement[2] = b->displacement[2];
}
void func_8001C9BC_1D5BC(struct GraphicsPoseFields *a, struct GraphicsPoseFields *b) {
    a->position[0] = b->position[0];
    a->position[1] = b->position[1];
    a->position[2] = b->position[2];
}
void func_8001C9D8_1D5D8(struct GraphicsPoseFields *a, struct GraphicsPoseFields *b) {
    a->position[0] += b->position[0];
    a->position[1] += b->position[1];
    a->position[2] += b->position[2];
}
