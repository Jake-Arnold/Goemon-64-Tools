/* Ganbare Goemon Japan-0, scheduler task callback machinery.
 * 15 original function addresses; 0x80034E74..0x8003502B inclusive,
 * decompressed ROM 0x35A74..0x35C2B, 0x1B8 bytes.
 * Definitions reflect exact native MIPS code generation, not guessed symbols.
 * No game ROM bytes are included in this file.
 */
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
extern Task *D_80173294_173E94;

/* Set the current task's slot +0x08. */
void func_80034E74_35A74(void *callback) {
    D_80173294_173E94->callback08 = callback;
}
/* Set an explicitly provided task's slot +0x08. */
void func_80034E84_35A84(Task *task, void *callback) {
    task->callback08 = callback;
}
/* Set the current task's primary callback (+0x0C). */
void func_80034E8C_35A8C(void *callback) {
    D_80173294_173E94->callback0C = callback;
}
/* Set any task's primary callback (+0x0C). */
void func_80034E9C_35A9C(Task *task, void *callback) {
    task->callback0C = callback;
}
/* Set the current task's slot +0x10. */
void func_80034EA4_35AA4(void *callback) {
    D_80173294_173E94->callback10 = callback;
}
/* Set any task's slot +0x10. */
void func_80034EB4_35AB4(Task *task, void *callback) {
    task->callback10 = callback;
}
/* Run callback immediately on current task; restore previous afterwards. */
void func_80034EBC_35ABC(Callback callback) {
    D_80173294_173E94->callback14 = D_80173294_173E94->callback0C;
    D_80173294_173E94->callback0C = (void *)callback;
    ((Callback)D_80173294_173E94->callback0C)(D_80173294_173E94, D_80173294_173E94->data18);
    D_80173294_173E94->callback0C = D_80173294_173E94->callback14;
}
/* Run callback immediately on explicit task, restoring previous afterwards. */
void func_80034F1C_35B1C(Task *task, Callback callback) {
    task->callback14 = task->callback0C;
    task->callback0C = (void *)callback;
    callback(task, task->data18);
    task->callback0C = task->callback14;
}
void func_80034F84_35B84(Task *task, Callback callback);
/* Install and run the callback on the current task. */
void func_80034F5C_35B5C(Callback callback) {
    func_80034F84_35B84(D_80173294_173E94, callback);
}
/* Install and run callback on an explicit task. */
void func_80034F84_35B84(Task *task, Callback callback) {
    task->callback0C = (void *)callback;
    callback(task, D_80173294_173E94->data18);
}
/* Restore saved current-task callback and run it immediately. */
void func_80034FB4_35BB4(void) {
    D_80173294_173E94->callback0C = D_80173294_173E94->callback14;
    ((Callback)D_80173294_173E94->callback0C)(D_80173294_173E94, D_80173294_173E94->data18);
}
/* Restore saved current-task callback without calling it. */
void func_80034FF4_35BF4(void) {
    Task *task = D_80173294_173E94;
    task->callback0C = task->callback14;
}
/* Restore saved explicit-task callback without calling it. */
void func_80035008_35C08(Task *task) {
    task->callback0C = task->callback14;
}
/* Set saved callback for current task. */
void func_80035014_35C14(void *callback) {
    D_80173294_173E94->callback14 = callback;
}
/* Set saved callback for explicit task. */
void func_80035024_35C24(Task *task, void *callback) {
    task->callback14 = callback;
}
