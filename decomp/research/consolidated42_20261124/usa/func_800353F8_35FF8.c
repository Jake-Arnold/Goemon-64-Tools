typedef struct Task {unsigned char pad00[0x24];signed short timer24;} Task;
extern void func_800353B4_35FB4(Task *,void *);
extern void func_8003522C_35E2C(Task *,void *);
extern void func_80035430_36030(Task *,void *);
void func_800353F8_35FF8(Task *task, void *callback, signed short ticks) {
 task->timer24 = ticks;
 func_800353B4_35FB4(task, callback);
 func_8003522C_35E2C(task, (void *)func_80035430_36030);
}
