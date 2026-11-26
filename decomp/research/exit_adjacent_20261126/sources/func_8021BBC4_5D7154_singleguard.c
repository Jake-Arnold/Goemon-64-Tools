typedef unsigned char u8;
typedef unsigned int u32;
typedef struct {u8 pad[0x1c];float x,y,z;u8 pad2[8];u32 field30;} Obj;
extern float D_8023F224_5FA7B4;
extern u8 D_80073400_74000[];
extern Obj *func_80035B5C_3675C(void *,int,int);
extern void func_8021BA50_5D6FE0(void *,Obj *,int);
Obj *func_8021BBC4_5D7154(void *t,int arg){
    Obj *o=func_80035B5C_3675C(t,2,1);
    if(o!=0){
        {
            float f=D_8023F224_5FA7B4;
            o->field30=(u32)D_80073400_74000|0x40000000;
            o->x=f;
            o->y=f;
            o->z=f;
            func_8021BA50_5D6FE0(t,o,arg);
            return o;
        }
    }
    return 0;
}
