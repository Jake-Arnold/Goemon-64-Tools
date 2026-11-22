typedef unsigned int u32;
typedef unsigned char u8;
typedef struct Obj {u8 pad[0x74];void *callback;} Obj;
extern void func_80034E8C_35A8C(void *);
extern void func_80011268_11E68(void);
void func_800112C0_11EC0(Obj *o, void *callback) {
    if(o != 0) {
        o->callback = callback;
        func_80034E8C_35A8C(func_80011268_11E68);
    }
}
