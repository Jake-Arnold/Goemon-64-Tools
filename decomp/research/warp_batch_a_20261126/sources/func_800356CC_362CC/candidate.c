typedef unsigned short u16;
typedef unsigned char u8;
typedef struct Object {
    u8 pad0[8];
    float x,y,z;
    u16 r,s,t,pad1;
    float i,j,k,other;
    void *b,*c;
    u16 m; u8 pad2[6]; u16 n; u8 pad3[6];
    u16 field44; u8 pad4[6]; u16 field4c; u8 pad5[6];
    u16 field54; u8 pad6[6]; u16 field5c; u8 pad7[6];
    u8 field64,field65,pad8[2]; float field68,field6c,field70;
    unsigned field74,field78; u8 field7c,pad9; u16 field7e;
} Object;
typedef struct Task { u8 pad[0x1c]; Object *object; } Task;
extern u8 *g_system_ptr;
extern u8 D_C2D90[];
extern void func_80013DA8_149A8(Object *);
Task *func_800356CC_362CC(Task *a, void *b, void *c, float x,float y,float z,u16 r,u16 s,u16 t,float i,float j,float k,u16 m,u16 mode,u16 n) {
    Object *o;
    if (a != 0) {
        o = a->object;
        if (o != 0) {
            o->b=b;
            o->c=c;
            o->x=x;
            o->y=y;
            o->z=z;
            o->r=r;
            o->s=s;
            o->t=t;
            o->i=i;
            o->j=j;
            o->k=k;
            o->m=m;
            o->n=n;
            o->field44=mode;
            o->field4c=0;
            o->field54=0;
            o->field5c=0;
            func_80013DA8_149A8(o);
            o->field64=0;
            o->field65=0;
            o->field74=0;
            o->field78=0;
            o->field7c=0;
            o->field7e=0;
            o->other=0.0f;
            o->field68=0.0f;
            o->field6c=0.0f;
            o->field70=0.0f;
        }
    }
    return a;
}
