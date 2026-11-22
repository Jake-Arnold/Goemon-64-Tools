typedef struct{char p[0x68];float f68,f6c,f70;char pad[0xE4-0x74];float e4,e8;}Actor_59E82C;extern void func_801E2950_59E860();void func_801E291C_59E82C(Actor_59E82C*a){a->f70=0.0f;a->f6c=0.0f;a->f68=0.0f;a->e4=0.0f;a->e8=0.0f;func_801E2950_59E860(a);}
extern void func_80038BC8_397C8(unsigned);typedef struct{char p[0x2C];unsigned char flag;}Inner_59E860;typedef struct{char p[0x5C];Inner_59E860*inner;}Actor_59E860;void func_801E2950_59E860(Actor_59E860*a){a->inner->flag=0;func_80038BC8_397C8(526);func_80038BC8_397C8(587);}
extern void func_801E291C_59E82C();void func_801E2980_59E890(void*a){ func_801E291C_59E82C(a); }

