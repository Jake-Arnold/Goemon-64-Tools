typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 pad[0x1c]; float x,y,z; } Obj;
typedef struct { u8 pad[0x5e]; u16 id; u32 a,b; u8 pad68[0x4c]; u32 b4; } Task;
extern float D_8023EE38_5FA3C8;
extern void func_80219E30_5D53C0(void);
extern void func_80034E8C_35A8C(void (*)(void));
extern void func_802268B8_5E1E48(Task *);
extern void func_8022697C_5E1F0C(Task *,int,float,int);
extern char func_8021EBE0_5DA170;
void func_80219EF4_5D5484(Task *t,Obj *o) {
    func_802268B8_5E1E48(t);
    func_8022697C_5E1F0C(t,0,0.33333334f,1);
    o->x=o->y=o->z=0.1f;
    ((void (*)(Task *,int,int))&func_8021EBE0_5DA170)(t,10,0);
    func_80034E8C_35A8C(func_80219E30_5D53C0);
}
