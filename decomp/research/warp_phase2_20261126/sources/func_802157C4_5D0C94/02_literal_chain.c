typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 pad[0x1c]; float x,y,z; } Obj;
typedef struct { u8 pad[0x5e]; u16 id; u32 a,b; u8 pad68[0x4c]; u32 b4; } Task;
extern float D_8023A238_5F5708;
extern void func_80215830_5D0D00(void);
extern void func_8003521C_35E1C(void (*)(void));
extern void func_80216DF8_5D22C8(Task *,int);
void func_802157C4_5D0C94(Task *t,Obj *o) {
    t->id=0x7e;
    func_80216DF8_5D22C8(t,8);
    o->x=o->y=o->z=0.2f;
    t->a=0x20;
    t->b=2;
    func_8003521C_35E1C(func_80215830_5D0D00);
}
