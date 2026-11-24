typedef struct { char pad[8]; float x,y,z; } Position;
typedef struct { char pad[4]; float sx,sy,sz,ox,oy,oz; int nx,ny,nz; char rest[0x108]; Position *pos; } Stage;
extern Stage D_8015CC30_15D830;
extern void func_8020D36C_5C883C(void *,int,int,int);
void func_8020D2A0_5C8770(void *task) {
    Stage *s = &D_8015CC30_15D830;
    Position *p = s->pos;
    int nx=s->nx,ny=s->ny,nz=s->nz;
    float half=(float)2;
    int x = (int)((p->x-s->ox)/s->sx + (float)nx/half);
    int y = (int)((p->y-s->oy)/s->sy + (float)ny/half);
    int z = (int)((p->z-s->oz)/s->sz + (float)nz/half);
    func_8020D36C_5C883C(task,x,y,z);
}
