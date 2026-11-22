/* Japanese original-address code; research only */
typedef unsigned char u8;typedef unsigned short u16;
typedef struct Obj{u8 pad[0xBC];void *cb;u8 pad2[2];u16 kind;} Obj;
extern int func_80222718_5DDCA8(void*,u16,int);extern void func_80034E8C_35A8C(void*);
void func_80226CA4_5E2234(Obj *o,void *arg1){
    if(func_80222718_5DDCA8(o,o->kind,12)!=0)func_80034E8C_35A8C(o->cb);
}
