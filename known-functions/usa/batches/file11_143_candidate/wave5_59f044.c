typedef struct Actor_59F068 Actor_59F068;
typedef struct {short code;} Inner_59F044;typedef struct {char pad[0x5C];Inner_59F044*state;} Actor_59F044;extern void func_801E3158_59F068(Actor_59F068*);void func_801E3134_59F044(Actor_59F044*p){p->state->code=0;func_801E3158_59F068((Actor_59F068*)p);}

typedef unsigned char u8;struct Actor_59F068 {char p[0x30];u8 flags;char pad[0xD4-0x31];u8 mode;};void func_801E3158_59F068(Actor_59F068*a){a->mode=60;a->flags&=~1;a->flags|=4;}

extern void func_801E32D4_59F1E4(void *,float,float,float);void func_801E3178_59F088(void*a){func_801E32D4_59F1E4(a,0,1.0f,1.0f);}
