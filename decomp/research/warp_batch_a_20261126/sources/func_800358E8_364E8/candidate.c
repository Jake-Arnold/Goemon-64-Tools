typedef unsigned short u16;
typedef void *Task;
extern Task func_800357BC_363BC(Task, void *, void *, void *, float, float, float, u16, u16, u16, float, float, float, u16, u16);
extern Task func_80034D24_35924(Task);
Task func_800358E8_364E8(Task a, void *b, void *c, void *d, float x, float y, float z, u16 r, u16 s, u16 t, float i, float j, float k, u16 m, u16 n) {
    return func_80034D24_35924(func_800357BC_363BC(a, b, c, d, x, y, z, r, s, t, i, j, k, m, n));
}
