typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 pad[0x5e]; u16 id; u32 a,b; } Task;
typedef struct { u8 pad[0x1c]; float x,y,z; } Object;
extern float D_8023A234_5F5704;
extern void func_80215230_5D0700(void);
extern void func_8003521C_35E1C(void (*)(void));
void func_802151E0_5D06B0(Task *t,Object *o) {
    float f=D_8023A234_5F5704;
    t->id=0x7e;
    o->x=f;
    o->y=f;
    o->z=f;
    t->a=0x20;
    t->b=2;
    func_8003521C_35E1C(func_80215230_5D0700);
}
