typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct Task {
    unsigned char pad00[0x22];
    u16 active22;
    unsigned char pad24[0x5C-0x24];
    u32 group[37];
} Task;
extern void func_80034D34_35934(Task *);
extern void func_80035ED0_36AD0(Task *);
void func_80034E04_35A04(Task *task, void *arg) {
    func_80034D34_35934(task);
}
void func_80034E24_35A24(Task *task) {
    s16 index;
    func_80035ED0_36AD0(task);
    task->active22 = 1;
    for (index = 0; index < 37; index++) {
        task->group[index] = 0;
    }
}
