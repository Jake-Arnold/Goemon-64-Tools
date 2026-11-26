typedef unsigned short u16;
typedef void *Task;
extern Task func_8003492C_3552C(Task, void *, int, u16);
extern Task func_800355D4_361D4(Task, void *, void *, float, float, float, u16, u16, u16, float, float, float, u16, u16);
Task func_8003542C_3602C(Task a, void *b, void *c, void *d, float x, float y, float z, u16 r, u16 s, u16 t, float i, float j, float k, u16 m, u16 n) {
    Task p = func_8003492C_3552C(a, b, 2, m);
    func_800355D4_361D4(p, c, d, x, y, z, r, s, t, i, j, k, m, n);
    return p;
}
