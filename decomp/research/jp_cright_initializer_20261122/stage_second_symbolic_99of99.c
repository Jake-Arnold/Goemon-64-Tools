typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;
typedef float f32;
extern u8 D_80162420_163020[];
extern u8 g_system[];
extern u8 D_3B07A[];
extern u8 *g_system_ptr;
extern void func_802189E8_5D3F78(void);
extern void *func_80034A78_35678(void *, void (*)(void), int);
extern void *func_80034A48_35648(void (*)(void), int);
extern void func_80023BA4_247A4(void);
extern void func_80034E8C_35A8C(void (*)(void));
extern void func_802126A0_5CDC30(void);
#define P(off) (*(void **)(D_80162420_163020+(off)))
#define U32(off) (*(u32 *)(D_80162420_163020+(off)))
#define U16(off) (*(u16 *)(D_80162420_163020+(off)))
#define U8(off) (*(u8 *)(D_80162420_163020+(off)))
#define F32(off) (*(f32 *)(D_80162420_163020+(off)))

void func_80212514_5CDAA4(void *current, void *other) {
    g_system_ptr=g_system;
    P(0x8C)=current;
    U8(0xD8)=1;
    U16(0x10A)=0;
    U32(0xB0)=20;
    U32(0xB4)=15;
    U32(0xB8)=20;
    U32(0xBC)=5;
    U32(0xC0)=20;
    U32(0xCC)=60;
    F32(0x104)=1.0f;
    if ((*(u16 *)(g_system_ptr+0x3B07A) & 1) != 0) {
        P(0x90)=current;
        P(0x94)=current;
        P(0x98)=current;
        P(0x9C)=current;
        P(0xA0)=current;
        P(0xA4)=current;
        P(0xA8)=current;
        U8(0xD1)=1;
        P(0xAC)=current;
    } else {
        P(0x94)=func_80034A78_35678(P(0x90),func_802189E8_5D3F78,0);
        P(0x98)=func_80034A48_35648(func_802189E8_5D3F78,0);
        P(0x9C)=func_80034A48_35648(func_802189E8_5D3F78,0);
        P(0xA0)=func_80034A48_35648(func_802189E8_5D3F78,0);
        P(0xA4)=func_80034A78_35678(P(0xA0),func_802189E8_5D3F78,0);
        P(0xA8)=func_80034A78_35678(P(0x90),func_802189E8_5D3F78,0);
        P(0xAC)=func_80034A78_35678(P(0xA0),func_802189E8_5D3F78,0);
        func_80023BA4_247A4();
        U32(0x158)=0;
        U32(0x15C)=0;
        if ((*(u16 *)(g_system_ptr+(u32)D_3B07A) & 8) != 0) {
            U8(0xD1)=1;
        }
        func_80034E8C_35A8C(func_802126A0_5CDC30);
    }
}
