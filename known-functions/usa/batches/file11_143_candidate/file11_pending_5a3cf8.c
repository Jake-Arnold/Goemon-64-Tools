typedef struct {char pad[0x86];unsigned short flag;} Inner;typedef struct {char pad[0x5C];Inner* state;unsigned char character;} Actor;
int func_801E7DE8_5A3CF8(Actor*a){return a->character==1 && a->state->flag==0xffff;}
