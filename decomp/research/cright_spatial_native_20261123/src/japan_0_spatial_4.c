typedef struct { char pad[8]; float x,y,z; } Position;
typedef struct { char pad[4]; float sx,sy,sz,ox,oy,oz; int nx,ny,nz; char rest[0x108]; Position *pos; } Stage;
extern Stage D_80162420_163020;
extern void func_8021215C_5CD6EC(void *,int,int,int);
void func_80212090_5CD620(void *task) {
    Stage *s = &D_80162420_163020;
    Position *p = s->pos;
    int nx=s->nx,ny=s->ny,nz=s->nz;
    float half=2.0f;
    int x = (int)((p->x-s->ox)/s->sx + (float)nx/half);
    int y = (int)((p->y-s->oy)/s->sy + (float)ny/half);
    int z = (int)((p->z-s->oz)/s->sz + (float)nz/half);
    func_8021215C_5CD6EC(task,x,y,z);
}
