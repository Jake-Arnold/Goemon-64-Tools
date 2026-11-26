typedef unsigned char u8;
typedef struct {u8 pad[0x1c]; float x,y,z;} Obj;
typedef struct {u8 pad[0x18]; Obj *child;} Task;
extern float D_8023A510_5F59E0;
extern void func_80216CE0_5D21B0(Task *, Obj *, int);
void func_80216E1C_5D22EC(Task *task,int kind) {
    Obj *obj;
    float value;
    value=D_8023A510_5F59E0;
    obj=task->child;
    obj->x=value;
    obj->y=value;
    obj->z=value;
    func_80216CE0_5D21B0(task,obj,kind);
}
