typedef struct Task {
    unsigned int next;
    unsigned int unknown04;
    void *callback08;
    void *callback0C;
    void *callback10;
    void *callback14;
    void *data18;
} Task;
typedef void (*Callback)(Task *, void *);
void func_800352AC_35EAC(Task *task, Callback callback) {
    task->callback14 = task->callback0C;
    task->callback0C = (void *)callback;
    callback(task, task->data18);
    task->callback0C = task->callback14;
}
