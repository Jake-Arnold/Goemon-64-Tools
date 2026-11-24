typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;
typedef float f32;
extern u8 D_8008CCC0_8D8C0[];
extern u8 *D_8015C5C8_15D1C8;
extern u8 D_8015CC30_15D830[];
extern void func_80213C50_5CF120(void);
extern void *func_80034E08_35A08(void *, void (*)(void), int);
extern void *func_80034DD8_359D8(void (*)(void), int);
extern void func_80023EE4_24AE4(void);
extern void func_8003521C_35E1C(void (*)(void));
extern void func_8020D848_5C8D18(void);
#define P(o) (*(void **)(D_8015CC30_15D830+(o)))
#define U32(o) (*(u32 *)(D_8015CC30_15D830+(o)))
#define U16(o) (*(u16 *)(D_8015CC30_15D830+(o)))
#define U8(o) (*(u8 *)(D_8015CC30_15D830+(o)))
#define F32(o) (*(f32 *)(D_8015CC30_15D830+(o)))
void func_8020D724_5C8BF4(void *current, void *other) {
    D_8015C5C8_15D1C8 = D_8008CCC0_8D8C0;
    U8(0xD8)=1;
    U16(0x10A)=0;
    U32(0xB0)=20;
    U32(0xB4)=15;
    U32(0xB8)=20;
    U32(0xBC)=5;
    U32(0xC0)=20;
    U32(0xCC)=60;
    P(0x8C)=current;
    F32(0x104)=1.0f;
    P(0x94)=func_80034E08_35A08(P(0x90),func_80213C50_5CF120,0);
    P(0x98)=func_80034DD8_359D8(func_80213C50_5CF120,0);
    P(0x9C)=func_80034DD8_359D8(func_80213C50_5CF120,0);
    P(0xA0)=func_80034DD8_359D8(func_80213C50_5CF120,0);
    P(0xA4)=func_80034E08_35A08(P(0xA0),func_80213C50_5CF120,0);
    P(0xA8)=func_80034E08_35A08(P(0x90),func_80213C50_5CF120,0);
    P(0xAC)=func_80034E08_35A08(P(0xA0),func_80213C50_5CF120,0);
    func_80023EE4_24AE4();
    U32(0x158)=0;
    U32(0x15C)=0;
    func_8003521C_35E1C(func_8020D848_5C8D18);
}
