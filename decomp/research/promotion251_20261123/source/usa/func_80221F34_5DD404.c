/* Japanese original-address code; research only */
typedef unsigned char u8;typedef unsigned short u16;
typedef struct Obj{u8 pad[0xBC];void *cb;u8 pad2[2];u16 kind;} Obj;
extern int func_8021D9A8_5D8E78(void*,u16,int);extern void func_8003521C_35E1C(void*);
void func_80221F34_5DD404(Obj *o,void *arg1){
    if(func_8021D9A8_5D8E78(o,o->kind,12)!=0)func_8003521C_35E1C(o->cb);
}
