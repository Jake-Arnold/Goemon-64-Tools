typedef struct {char pad30[0x30];unsigned char f30;char pad48[0x48-0x31];unsigned f48;unsigned char f4c;char pad4e;unsigned short f4e,f50,f52;} Actor;
void func_801EE228_5AA138(Actor*a,int x,int y,int z,int b,int c,int d){if(a){a->f30=x;a->f48=y;a->f4c=z;a->f4e=b;a->f50=c;a->f52=d;}}
