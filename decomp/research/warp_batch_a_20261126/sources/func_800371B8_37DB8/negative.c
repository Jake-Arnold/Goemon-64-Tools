typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 a[0x2DE4]; u8 state; u8 b[0xF]; u16 index; } Partial;
typedef struct { u8 a[0x3AE04]; u32 value; u8 b[0x1D8]; u16 scene,mode,x,y; short z; u16 heading; } Tail;
extern u8 *g_system_ptr;
extern Tail g_system;
extern u32 D_80162020_162C20[], D_80162030_162C30[];
extern u8 D_3AFE0[];
extern void func_8000364C_424C(int);
void func_800371B8_37DB8(void) {
    u8 *system;
    Partial *p;
    int one=2;
    func_8000364C_424C(12);
    system=g_system_ptr;
    p=(Partial *)(system+0x38000);
    if(p->state==4) {
        D_80162020_162C20[p->index]=one;
        *(u16 *)(system+(unsigned int)D_3AFE0)=p->index+0x221;
    } else {
        D_80162030_162C30[p->index]=one;
        switch(p->index) {
        case 0:
            break;
        case 1:
            g_system.scene=0x132;
            g_system.mode=0;
            g_system.x=0x6C4;
            g_system.y=0x1B2;
            g_system.z=5;
            g_system.heading=0x200;
            break;
        case 2:
            g_system.value=0x49;
            g_system.scene=0x14D;
            g_system.mode=0;
            g_system.x=0xE1;
            g_system.y=0x202;
            g_system.z=-0x1F3;
            g_system.heading=0x200;
            break;
        case 3:
            break;
        }
    }
}
