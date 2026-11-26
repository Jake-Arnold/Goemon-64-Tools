typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 pad[0x1c]; float x,y,z; } Obj;
typedef struct { u8 pad[0x5e]; u16 id; u32 a,b; u8 pad68[0x4c]; u32 b4; } Task;
extern const float D_8023EF48_5FA4D8;
extern void func_8021A5C0_5D5B50(void);
extern void func_80034E8C_35A8C(void (*)(void));
extern void func_8021BB68_5D70F8(Task *,int);
void func_8021A554_5D5AE4(Task *t,Obj *o) {
    float f;
    t->id=0x7e;
    func_8021BB68_5D70F8(t,8);
    f=D_8023EF48_5FA4D8;
    o->x=o->y=o->z=f;
    t->a=0x20;
    t->b=2;
    func_80034E8C_35A8C(func_8021A5C0_5D5B50);
}
