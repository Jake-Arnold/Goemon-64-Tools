/* Original-USA file_12 runtime callback; isolated IDO 5.3 research only.
 * reserved[] deliberately fixes original stack-frame geometry; it is not
 * evidence of an actual runtime array or source-level gameplay storage. */
typedef unsigned char u8;
typedef unsigned int u32;
typedef struct Placement {u8 pad[0x10]; u8 active;} Placement;
typedef struct Actor {u8 pad0[0x34]; u32 field34; u32 field38; u8 pad1[0x2c]; u32 state; u8 pad2[0x4]; Placement* placement; u8 pad3[2]; u8 range; u8 field77;} Actor;
extern void func_80218E7C_5D434C(Actor *);
extern void func_80034ED4_35AD4(void);
extern Actor *func_80034E08_35A08(void *, void *, int);
extern void func_80035244_35E44(Actor *, void *);
extern void func_80213ED0_5CF3A0(void);
extern void *D_8015CCBC;
void func_80218F30_5D4400(Actor *actor, void *user) {
   volatile int reserved[3];
   Placement *placement;
   int range;
   Actor *created;
   func_80218E7C_5D434C(actor);
   actor->field38=0;
   actor->field34=0;
   if (actor->state & 2) {
     placement=actor->placement;
     range=actor->range;
     func_80034ED4_35AD4();
     if (placement) {
       created=func_80034E08_35A08(D_8015CCBC,func_80213ED0_5CF3A0,0);
       if (created) {
         created->field77=0;
         created->placement=placement;
         created->state=8;
         created->range=range+5;
         func_80035244_35E44(created,func_80218F30_5D4400);
       } else placement->active=0;
     }
   }
}
