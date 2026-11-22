extern char D_CF8F0;
typedef struct {char pad[0x22];unsigned short flags;} State;
extern unsigned D_8015C5C8_15D1C8;

void func_801FC590_5B84A0(void){State *s=*(State **)(D_8015C5C8_15D1C8 + (unsigned)&D_CF8F0);if(s){s->flags &= ~0x14;}}

extern unsigned D_8015C5C8_15D1C8;

void func_801FC5C0_5B84D0(void){State *s=*(State **)(D_8015C5C8_15D1C8 + (unsigned)&D_CF8F0);if(s){s->flags |= 0x14;}}

