typedef struct Task Task;
typedef unsigned short u16;
extern Task *D_80173294_173E94;
extern void func_8003492C_3552C(Task *, void *, int, u16);
void func_800348BC_354BC(void *arg, u16 value) {
    func_8003492C_3552C(D_80173294_173E94, arg, 1, value);
}
void func_800348F4_354F4(void *arg, u16 value) {
    func_8003492C_3552C(D_80173294_173E94, arg, 2, value);
}
