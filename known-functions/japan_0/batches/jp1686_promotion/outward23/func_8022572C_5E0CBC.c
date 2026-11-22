typedef unsigned int u32;
typedef unsigned char u8;
typedef struct Obj {u8 pad68[0x68];u32 flags;u8 other[0x48];void *callback;} Obj;
extern void func_80034E8C_35A8C(void *);
void func_8022572C_5E0CBC(Obj *o, void *arg1) {
    o->flags |= 0x4400;
    func_80034E8C_35A8C(o->callback);
}
