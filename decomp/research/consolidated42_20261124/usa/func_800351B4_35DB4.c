typedef signed short s16;typedef unsigned short u16;typedef unsigned int u32;
typedef struct Task {unsigned char pad00[0x22];u16 active22;unsigned char pad24[0x5C-0x24];u32 group[37];} Task;
extern void func_80036260_36E60(Task *);
void func_800351B4_35DB4(Task *task) {
 s16 index;
 func_80036260_36E60(task);
 task->active22 = 1;
 for (index = 0; index < 37; index++) {task->group[index] = 0;}
}
