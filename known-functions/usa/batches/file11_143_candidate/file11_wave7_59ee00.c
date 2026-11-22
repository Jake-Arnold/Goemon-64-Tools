typedef struct {char pad[0x2c];unsigned char flag;} Inner_59EE00;typedef struct {char pad[0x4c];unsigned char mode;char gap[0x5c-0x4d];Inner_59EE00*state;char reserved[0x68-0x60];float a,b,c;char gap2[0xe4-0x74];float d,e;} Actor_59EE00;void func_801E2EF0_59EE00(Actor_59EE00*p,unsigned unused){p->d=0.0f;p->e=0.0f;p->mode=20;p->state->flag=0;}

typedef struct {char pad[0x2c];unsigned char flag;} Inner_59EE24;typedef struct {char pad[0x4c];unsigned char mode;char gap[0x5c-0x4d];Inner_59EE24*state;char reserved[0x68-0x60];float a,b,c;char gap2[0xe4-0x74];float d,e;} Actor_59EE24;void func_801E2F14_59EE24(Actor_59EE24*p){p->d=0.0f;p->e=0.0f;p->c=0.0f;p->b=0.0f;p->a=0.0f;p->state->flag=0;}

typedef struct {char pad[0x2C];unsigned char flag;} Inner_59EE48;typedef struct {char pad[0x5C];Inner_59EE48* state;} Actor_59EE48;void func_801E2F38_59EE48(Actor_59EE48*a){a->state->flag=0;}

