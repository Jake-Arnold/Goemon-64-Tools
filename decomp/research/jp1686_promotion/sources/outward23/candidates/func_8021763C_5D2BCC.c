typedef unsigned int u32;
typedef unsigned char u8;
typedef struct Obj {u8 pad[0x64];u32 flags;} Obj;
extern void func_80034E8C_35A8C(void *);
extern void func_80217674_5D2C04(void);
void func_8021763C_5D2BCC(Obj *o, void *ignored) {
    o->flags |= 2;
    func_80034E8C_35A8C(func_80217674_5D2C04);
}
