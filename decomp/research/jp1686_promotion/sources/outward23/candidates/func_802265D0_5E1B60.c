/* Japanese original-address code; research only */
typedef unsigned char u8;typedef unsigned short u16;
typedef struct Obj{u8 pad[0xA4];u16 kind;} Obj;
extern void func_8003CF80_3DB80(u16);extern void func_80034E8C_35A8C(void*);extern void func_8022659C_5E1B2C(void);
void func_802265D0_5E1B60(Obj *o,void *arg1){
    func_8003CF80_3DB80(o->kind);
    func_80034E8C_35A8C(func_8022659C_5E1B2C);
}
