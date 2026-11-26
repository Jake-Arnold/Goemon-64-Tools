typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {
    u8 pad0[4];
    u8 field4,field5,pad6[2];
    union {u32 word;struct {u32 top:3;u32 rest:2;u32 enable:1;u32 remain:7;u32 mode:4;u32 tail:15;} bits;struct {u8 flags,pad[3];} bytes;} p;
    u8 padc[4];
    u8 field10,pad11[0xB];
    u16 field1c,pad1e;
    u16 field20,pad22;
    u8 pad24[8];
    float x,y;
} Obj;
void func_8021AEF4_5D6484(Obj *o,u16 a,u16 b) {
    o->p.bits.enable=1;
    o->field4=1;
    o->p.bits.top=2;
    o->x=(float)(u16)a;
    o->y=(float)(u16)b;
    o->field5=10;
    o->field1c=16;
    o->field20=16;
    o->p.bits.mode=6;
    o->field10=0;
}
