typedef signed short u16;
typedef void *Task;
extern Task func_80034CBC_358BC(Task, void *, int, u16);
extern Task func_80035964_36564(Task, void *, void *, float, float, float, u16, u16, u16, float, float, float, u16, u16);
Task func_800357BC_363BC(Task a, void *b, void *c, void *d, float x, float y, float z, u16 r, u16 s, u16 t, float i, float j, float k, u16 m, u16 n) {
    Task p = func_80034CBC_358BC(a, b, 2, m);
    func_80035964_36564(p, c, d, x, y, z, r, s, t, i, j, k, m, n);
    return p;
}
