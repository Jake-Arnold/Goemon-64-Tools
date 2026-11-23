/* Japanese original-address code; research only */
typedef unsigned char u8;typedef unsigned short u16;
typedef struct Obj{u8 pad[0x8A];u16 counter;u8 pad2[0x30];void *cb;} Obj;
extern void func_8003521C_35E1C(void*);
void func_80222B30_5DE000(Obj *o,void *arg1){
    o->counter--;
    if(o->counter==0)func_8003521C_35E1C(o->cb);
}
