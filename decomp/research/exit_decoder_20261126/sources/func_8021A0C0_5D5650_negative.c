typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef union { u32 w; struct {s16 x,y;} h; struct {s8 a,b,c,d;} b; } Word;
typedef struct { u8 pad[0xd0]; u32 a,b,c; } Exit;
typedef struct { u8 pad[0x3AE00]; u16 D_3AE00; u8 p1[0x21]; u8 D_3AE23; u8 p2[5]; u8 D_3AE29; u8 p3[0x1b6]; u16 D_3AFE0; s16 D_3AFE2,D_3AFE4,D_3AFE6,D_3AFE8,D_3AFEA; } Sys;
extern Sys *g_system_ptr;
extern int func_80023D9C_2499C(int);
#define H(s) (g_system_ptr->s)
#define UH(s) (g_system_ptr->s)
#define B(s) (g_system_ptr->s)
void func_8021A0C0_5D5650(Exit *p) {
    Word a,b,c;
    a.w=p->a;
    b.w=p->b;
    c.w=p->c;
    H(D_3AFE0)=a.h.x;
    if (UH(D_3AFE0)!=0x1c4) goto normal;
    if (func_80023D9C_2499C(0x17)) {
        H(D_3AFE0)=0x1cf;
        H(D_3AFE4)=0x52;
        H(D_3AFE6)=-0x31;
        H(D_3AFE8)=0xa7;
        H(D_3AFEA)=c.h.x;
        H(D_3AE00)=c.b.c&0xf;
        H(D_3AFE2)=c.b.d;
    } else {
normal:
        H(D_3AFE4)=a.h.y;
        H(D_3AFE6)=b.h.x;
        H(D_3AFE8)=b.h.y;
        H(D_3AFEA)=c.h.x;
        H(D_3AE00)=c.b.c&0xf;
        H(D_3AFE2)=c.b.d;
    }
    B(D_3AE23)=1;
    B(D_3AE29)++;
}
