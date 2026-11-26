typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 pad[0x1c]; float x,y,z; } Obj;
typedef struct { u8 pad[0x5e]; u16 id; u32 a,b; u8 pad68[0x4c]; u32 b4; } Task;
extern volatile float D_8023A124_5F55F4;
extern void func_802150A0_5D0570(void);
extern void func_8003521C_35E1C(void (*)(void));
extern void func_80221B48_5DD018(Task *);
extern void func_80221C0C_5DD0DC(Task *,int,float,int);
extern char func_80219E70_5D5340;
void func_802150E4_5D05B4(Task *t,Obj *o) {
    float f;
    func_80221B48_5DD018(t);
    func_80221C0C_5DD0DC(t,0,0.33333334f,1);
    f=D_8023A124_5F55F4;
    o->x=o->y=o->z=f;
    ((void (*)(Task *,int,int))&func_80219E70_5D5340)(t,10,0);
    t->b4=0;
    func_8003521C_35E1C(func_802150A0_5D0570);
}
