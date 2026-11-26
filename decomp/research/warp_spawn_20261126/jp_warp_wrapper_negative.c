typedef signed short u16;
typedef void *Task;
extern Task func_8003542C_3602C(Task, void *, void *, void *, float, float, float, u16, u16, u16, float, float, float, u16, u16);
extern Task func_80034994_35594(Task);
Task func_80035558_36158(Task a, void *b, void *c, void *d, float x, float y, float z, u16 r, u16 s, u16 t, float i, float j, float k, u16 m, u16 n) {
    return func_80034994_35594(func_8003542C_3602C(a, b, c, d, x, y, z, r, s, t, i, j, k, m, n));
}
