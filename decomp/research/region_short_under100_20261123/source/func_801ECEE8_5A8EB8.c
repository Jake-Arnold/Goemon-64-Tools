typedef struct {char pad[0x86];unsigned short flag;} Inner;
typedef struct {char pad[0x5C];Inner* state;unsigned char character;} Actor;
int func_801ECEE8_5A8EB8(Actor*a){return (a->character==0) && (a->state->flag!=0);}
