typedef unsigned char u8;
typedef struct {u8 pad[0x1c]; float x,y,z;} Obj;
typedef struct {u8 pad[0x18]; Obj *child;} Task;
extern float D_8023F220_5FA7B0;
extern void func_8021BA50_5D6FE0(Task *, Obj *, int);
void func_8021BB8C_5D711C(Task *task,int kind) {
    Obj *obj;
    float value;
    value=D_8023F220_5FA7B0;
    obj=task->child;
    obj->x=value;
    obj->y=value;
    obj->z=value;
    func_8021BA50_5D6FE0(task,obj,kind);
}
