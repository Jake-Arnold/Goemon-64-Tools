typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef union { u32 w; struct {s16 x,y;} h; struct {s8 a,b,c,d;} b; } Word;
typedef struct { u8 pad[0xd0]; u32 a,b,c; } Exit;
typedef struct { u8 pad[0x3AE00]; u16 D_3AE00; u8 p1[0x21]; u8 D_3AE23; u8 p2[5]; u8 D_3AE29; u8 p3[0x1b6]; u16 D_3AFE0; s16 D_3AFE2,D_3AFE4,D_3AFE6,D_3AFE8,D_3AFEA; } Sys;
extern Sys *D_8015C5C8_15D1C8;
extern int func_800240DC_24CDC(int);
#define H(s) (D_8015C5C8_15D1C8->s)
#define UH(s) (D_8015C5C8_15D1C8->s)
#define B(s) (D_8015C5C8_15D1C8->s)
void func_80215330_5D0800(Exit *p) {
    Word a,b,c;
    a.w=p->a;
    b.w=p->b;
    c.w=p->c;
    H(D_3AFE0)=a.h.x;
    if (UH(D_3AFE0)!=0x1c4) goto normal;
    if (func_800240DC_24CDC(0x17)) {
        H(D_3AFE0)=0x1cf;
        H(D_3AFE4)=0x52;
        H(D_3AFE6)=-0x32;
        H(D_3AFE8)=0xa7;
        H(D_3AFEA)=c.h.x;
        H(D_3AE00)=c.b.c&0x7;
        H(D_3AFE2)=c.b.d;
    } else {
normal:
        H(D_3AFE4)=a.h.y;
        H(D_3AFE6)=b.h.x;
        H(D_3AFE8)=b.h.y;
        H(D_3AFEA)=c.h.x;
        H(D_3AE00)=c.b.c&0x7;
        H(D_3AFE2)=c.b.d;
    }
    B(D_3AE23)=1;
    B(D_3AE29)++;
}
