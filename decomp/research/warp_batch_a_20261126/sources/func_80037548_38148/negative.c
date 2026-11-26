typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 a[0x2DE4]; u8 state; u8 b[0xF]; u16 index; } Partial;
typedef struct { u8 a[0xAE04]; u32 value; u8 b[0x1D8]; u16 scene,mode,x,y; short z; u16 heading; } Tail;
extern u8 *D_8015C5C8_15D1C8;
extern Tail D_800BCCC0_BD8C0;
extern u32 D_8015C830_15D430[], D_8015C840_15D440[];
extern u8 D_3AFE0[];
extern void func_80003728_4328(int);
void func_80037548_38148(void) {
    u8 *system;
    Partial *p;
    int one=2;
    func_80003728_4328(12);
    system=D_8015C5C8_15D1C8;
    p=(Partial *)(system+0x38000);
    if(p->state==4) {
        D_8015C830_15D430[p->index]=one;
        *(u16 *)(system+(unsigned int)D_3AFE0)=p->index+0x221;
    } else {
        D_8015C840_15D440[p->index]=one;
        switch(p->index) {
        case 0:
            break;
        case 1:
            D_800BCCC0_BD8C0.scene=0x132;
            D_800BCCC0_BD8C0.mode=0;
            D_800BCCC0_BD8C0.x=0x6C4;
            D_800BCCC0_BD8C0.y=0x1B2;
            D_800BCCC0_BD8C0.z=5;
            D_800BCCC0_BD8C0.heading=0x200;
            break;
        case 2:
            D_800BCCC0_BD8C0.value=0x49;
            D_800BCCC0_BD8C0.scene=0x14D;
            D_800BCCC0_BD8C0.mode=0;
            D_800BCCC0_BD8C0.x=0xE1;
            D_800BCCC0_BD8C0.y=0x202;
            D_800BCCC0_BD8C0.z=-0x1F3;
            D_800BCCC0_BD8C0.heading=0x200;
            break;
        case 3:
            break;
        }
    }
}
