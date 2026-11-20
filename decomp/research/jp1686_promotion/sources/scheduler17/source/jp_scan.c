typedef struct Task { struct Task *next; } Task;
extern Task *D_80072E08_73A08;
void func_80034380_34F80(void) {
    Task *task = D_80072E08_73A08;
    if (task != 0) {
        do { task = task->next; } while (task != 0);
    }
}
