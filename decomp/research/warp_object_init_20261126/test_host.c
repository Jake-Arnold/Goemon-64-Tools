/* Actual-source host test; 32-bit layout assertions and portable semantic fixtures. */
#ifdef JAPAN
#include "jp_tail.c"
#define PRIMARY func_800355D4_361D4
#define SIBLING func_800356CC_362CC
#define SYSTEM g_system_ptr
#define CALLBACK func_80013DA8_149A8
#else
#include "usa_tail.c"
#define PRIMARY func_80035964_36564
#define SIBLING func_80035A5C_3665C
#define SYSTEM D_8015C5C8_15D1C8
#define CALLBACK func_80014218_14E18
#endif
static u8 sys[0xc2d92] __attribute__((aligned(2)));
u8 *SYSTEM = sys;
static Object obj;
static Task task;
static unsigned calls, errors;
static u16 expected;
#define CHECK(x) do { if (!(x)) ++errors; } while(0)
#if __SIZEOF_POINTER__ == 4
#define OFF(field,n) typedef char check_##field[__builtin_offsetof(Object,field)==(n)?1:-1]
OFF(x,8); OFF(y,12); OFF(z,16); OFF(r,20); OFF(i,28); OFF(other,40);
OFF(b,44); OFF(c,48); OFF(m,52); OFF(n,60); OFF(field44,68); OFF(field4c,76);
OFF(field54,84); OFF(field5c,92); OFF(field64,100); OFF(field68,104);
OFF(field74,116); OFF(field7e,126);
typedef char task_offset[__builtin_offsetof(Task,object)==0x1c?1:-1];
#endif
void CALLBACK(Object *o) {
    ++calls;
    CHECK(o==&obj); CHECK(o->field44==expected);
    CHECK(o->field4c==0 && o->field54==0 && o->field5c==0);
    /* The callback happens before these fields are cleared. */
    CHECK(o->field7e==0xffff && o->other==9.0f);
    o->field64=1; o->field65=1; o->field74=1; o->field78=1;
    o->field7c=1; o->field7e=1; o->other=1.0f;
    o->field68=1.0f; o->field6c=1.0f; o->field70=1.0f;
}
static void seed(void) {
    unsigned k; u8 *p=(u8 *)&obj;
    for(k=0;k<sizeof(obj);++k)p[k]=0xff;
    obj.other=9.0f;
}
static void post(u16 m,u16 n) {
    CHECK(obj.b==&task && obj.c==&obj);
    CHECK(obj.x==-1.25f && obj.y==2.5f && obj.z==-3.75f);
    CHECK(obj.r==0 && obj.s==0x8000 && obj.t==0xffff);
    CHECK(obj.i==0.125f && obj.j==1.0f && obj.k==-2.0f);
    CHECK(obj.m==m && obj.n==n && obj.field44==expected);
    CHECK(obj.field4c==0 && obj.field54==0 && obj.field5c==0);
    CHECK(obj.field64==0 && obj.field65==0 && obj.field74==0 && obj.field78==0);
    CHECK(obj.field7c==0 && obj.field7e==0 && obj.other==0.0f);
    CHECK(obj.field68==0.0f && obj.field6c==0.0f && obj.field70==0.0f);
    CHECK(obj.pad0[0]==0xff && obj.pad9==0xff);
}
static int exercise(void) {
    unsigned k; Task *p; unsigned status;
    p=PRIMARY(0,0,0,0,0,0,0,0,0,0,0,0,0,0); CHECK(p==0);
    p=SIBLING(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0); CHECK(p==0);
    task.object=0;
    p=PRIMARY(&task,0,0,0,0,0,0,0,0,0,0,0,0,0); CHECK(p==&task);
    p=SIBLING(&task,0,0,0,0,0,0,0,0,0,0,0,0,0,0); CHECK(p==&task); CHECK(calls==0);
    task.object=&obj;
    for(k=0;k<65536;k++) {
        expected=(u16)k; *(u16 *)(sys+0xc2d90)=expected; seed();
        p=PRIMARY(&task,&task,&obj,-1.25f,2.5f,-3.75f,0,0x8000,0xffff,0.125f,1.0f,-2.0f,(u16)k,(u16)~k); CHECK(p==&task); post((u16)k,(u16)~k);
        expected=(u16)~k; seed();
        p=SIBLING(&task,&task,&obj,-1.25f,2.5f,-3.75f,0,0x8000,0xffff,0.125f,1.0f,-2.0f,(u16)k,expected,(u16)~k); CHECK(p==&task); post((u16)k,(u16)~k);
    }
    CHECK(calls==131072); status=errors?1:0;
    return status;
}

#ifdef FREESTANDING32
void _start(void) {
    unsigned status=exercise();
    __asm__ volatile("int $0x80"::"a"(1),"b"(status):"memory");
    __builtin_unreachable();
}
#else
int main(void) { return exercise(); }
#endif
