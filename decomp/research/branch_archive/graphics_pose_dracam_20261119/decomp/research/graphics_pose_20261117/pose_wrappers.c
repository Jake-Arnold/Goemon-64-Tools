typedef unsigned int u32;
typedef unsigned short u16;
typedef struct {char pad0[8];u32 position[3];u16 rotation[3];u16 pad1;float translation[3];} Pose;
extern u16 D_801689F0_1695F0;
extern u16 D_801689F2_1695F2;
extern u16 D_801689F4_1695F4;
extern void func_8001E9B0_1F5B0(void *,u32,u32,u32,u16,u16,u16,float,float,float);
void func_8001E2BC_1EEBC(void *ctx, Pose *pose) {
 if (pose->rotation[0]==0x8000) {D_801689F0_1695F0 = 0;} else {D_801689F0_1695F0=pose->rotation[0];}
 if (pose->rotation[1]==0x8000) {D_801689F2_1695F2 = 0;} else {D_801689F2_1695F2=pose->rotation[1];}
 if (pose->rotation[2]==0x8000) {D_801689F4_1695F4 = 0;} else {D_801689F4_1695F4=pose->rotation[2];}
 func_8001E9B0_1F5B0(ctx,pose->position[0],pose->position[1],pose->position[2],
                      pose->rotation[0],pose->rotation[1],pose->rotation[2],
                      pose->translation[0],pose->translation[1],pose->translation[2]);
}

extern void func_8001EC04_1F804(void*,u32,u32,u32,u16,u16,u16,float,float,float);
void func_8001E380_1EF80(void* ctx, Pose *p) {
    func_8001EC04_1F804(ctx,p->position[0],p->position[1],p->position[2],
      p->rotation[0],p->rotation[1],p->rotation[2],
      p->translation[0],p->translation[1],p->translation[2]);
}
