typedef unsigned int u32;
typedef unsigned char u8;
typedef struct Obj {u8 pad[0x64];u32 flags;} Obj;
extern void func_80034E8C_35A8C(void *);
extern void func_802172B4_5D2844(void);
void func_8021727C_5D280C(Obj *o, void *ignored) {
    o->flags |= 2;
    func_80034E8C_35A8C(func_802172B4_5D2844);
}
