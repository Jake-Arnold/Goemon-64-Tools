typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 pad[0x5e]; u16 id; u32 a,b; } Task;
typedef struct { u8 pad[0x1c]; float x,y,z; } Object;
extern float D_8023EF44_5FA4D4;
extern void func_80219FC0_5D5550(void);
extern void func_80034E8C_35A8C(void (*)(void));
void func_80219F70_5D5500(Task *t,Object *o) {
    float f=D_8023EF44_5FA4D4;
    t->id=0x7f;
    o->x=f;
    o->y=f;
    o->z=f;
    t->a=0x20;
    t->b=2;
    func_80034E8C_35A8C(func_80219FC0_5D5550);
}
