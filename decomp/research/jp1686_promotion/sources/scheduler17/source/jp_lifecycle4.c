typedef struct Task Task;
extern Task *D_80173294_173E94;
extern void func_80034D34_35934(Task *);
extern void func_80035F4C_36B4C(Task *);
void func_80034CB4_358B4(Task *);
void func_80034C90_35890(void) {
    func_80034CB4_358B4(D_80173294_173E94);
}
void func_80034CB4_358B4(Task *task) {
    func_80034D34_35934(task);
}
void func_80034CD4_358D4(void) {
    func_80035F4C_36B4C(D_80173294_173E94);
    func_80034CB4_358B4(D_80173294_173E94);
}
void func_80034D04_35904(Task *task) {
    func_80035F4C_36B4C(D_80173294_173E94);
    func_80034D34_35934(task);
}
