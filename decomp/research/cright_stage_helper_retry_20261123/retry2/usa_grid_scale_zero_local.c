typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u16 id; } Definition;
typedef struct { char pad0[12]; Definition *def; u8 occupied; char pad1[3]; } Placement;
typedef struct { char pad0[0x68]; int mode; char pad1[4]; Placement *placement; } Task;
typedef struct { char pad0[0x1c]; int nx,ny,nz; char pad1[0x10]; u32 *grid; char pad2[4]; u16 res; char pad3[2]; int radius; } Stage;
extern Stage D_8015CC30_15D830;
extern Placement *D_8015CDDC;
extern Definition *D_8015CDE0;
extern u8 D_80229FE4_5E54B4[];
extern void *D_802287C0_5E3C90[];
extern u16 D_802297D6_5E4CA6[];
extern float D_80239A80_5F4F50;
extern char D_8006D920_6E520[];
extern void *func_80014840_15440(void *,u16);
extern void *func_80219CA0_5D5170(void *,int);
extern Task *func_80035690_36290(void *,void *,int,u32,float,float,float,int,int,int,float,float,float,int,int,int);
extern void func_80218A54_5D3F24(Task *,Placement *);
void func_8020D36C_5C883C(void *owner,int x,int y,int z) {
    Stage *s=&D_8015CC30_15D830;
    float scale=D_80239A80_5F4F50;
    float zero=0.0f;
    int radius=s->radius;
    int nx=s->nx,ny=s->ny,nz=s->nz;
    int i,j,k;
    Placement *p;
    Task *task;
    void *anchor;
    u16 id;
    for(i=x-radius; i<=x+radius; i++) {
        if(i<0 || i>=nx) continue;
        for(j=y-radius; j<=y+radius; j++) {
            if(j<0 || j>=ny) continue;
            for(k=z-radius; k<=z+radius; k++) {
                if(k<0 || k>=nz) continue;
                p=func_80014840_15440((void *)s->grid[i*ny*nz+j*nz+k],s->res);
                if(p) {
                    for(;;p++) {
                        D_8015CDDC=p;
                        if(p->occupied) continue;
                        D_8015CDE0=func_80014840_15440(p->def,s->res);
                        if(!D_8015CDE0) break;
                        anchor=func_80219CA0_5D5170(owner,D_80229FE4_5E54B4[D_8015CDE0->id-1]);
                        if(anchor) {
                            id=D_8015CDE0->id;
                            task=func_80035690_36290(anchor,D_802287C0_5E3C90[id-1],0,(u32)D_8006D920_6E520|0x40000000,zero,zero,zero,0,0,0,scale,scale,scale,0,0,D_802297D6_5E4CA6[id]);
                            if(task) { D_8015CDDC->occupied=1; func_80218A54_5D3F24(task,D_8015CDDC); task->mode=8; task->placement=D_8015CDDC; }
                        }
                    }
                }
                radius=s->radius;
            }
        }
    }
}
