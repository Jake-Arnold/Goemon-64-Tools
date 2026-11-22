typedef struct Task {
    unsigned int next;
    unsigned int unk04;
    void *callback08;
    void *callback0C;
    void *callback10;
    void *callback14;
    void *data18;
    unsigned char pad1C[8];
    signed short timer24;
} Task;
extern Task *D_80173294_173E94;
extern void func_80035024_35C24(Task *, void *);
extern void func_80034E9C_35A9C(Task *, void *);
extern void func_80034FF4_35BF4(void);
extern void func_80035124_35D24(Task *, void *);
void func_80035068_35C68(Task *, void *, signed short);
void func_800350A0_35CA0(Task *, void *);
void func_80035100_35D00(Task *);

void func_8003502C_35C2C(void *callback, signed short ticks) {
    func_80035068_35C68(D_80173294_173E94, callback, (signed short)ticks);
}
void func_80035068_35C68(Task *task, void *callback, signed short ticks) {
    task->timer24 = ticks;
    func_80035024_35C24(task, callback);
    func_80034E9C_35A9C(task, (void *)func_800350A0_35CA0);
}
void func_800350A0_35CA0(Task *task, void *arg) {
    task->timer24--;
    if (task->timer24 <= 0) func_80034FF4_35BF4();
}
void func_800350DC_35CDC(void) {
    func_80035100_35D00(D_80173294_173E94);
}
void func_80035100_35D00(Task *task) {
    func_80034E9C_35A9C(task, (void *)func_80035124_35D24);
}
