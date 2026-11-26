typedef unsigned char u8;
typedef unsigned int u32;
typedef struct {u8 pad[0x1c];float x,y,z;u8 pad2[8];u32 field30;} Obj;
extern float D_8023A514_5F59E4;
extern u8 D_8006D920_6E520[];
extern Obj *func_80035EEC_36AEC(void *,int,int);
extern void func_80216CE0_5D21B0(void *,Obj *,int);
Obj *func_80216E54_5D2324(void *t,int arg){
    Obj *o=func_80035EEC_36AEC(t,2,1);
    if(o!=0){
        if(o!=0){
            float f=D_8023A514_5F59E4;
            o->field30=(u32)D_8006D920_6E520|0x40000000;
            o->x=f;
            o->y=f;
            o->z=0.0f;
            func_80216CE0_5D21B0(t,o,arg);
            return o;
        }
    }
    return 0;
}
