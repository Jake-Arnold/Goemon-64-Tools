/* Japanese original-address code; research only */
typedef unsigned char u8;typedef unsigned short u16;
typedef struct Obj{u8 pad[0x8A];u16 counter;u8 pad2[0x30];void *cb;} Obj;
extern void func_80034E8C_35A8C(void*);
void func_802278A0_5E2E30(Obj *o,void *arg1){
    o->counter--;
    if(o->counter==0)func_80034E8C_35A8C(o->cb);
}
