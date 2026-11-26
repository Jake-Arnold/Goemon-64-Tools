typedef unsigned char u8;
typedef unsigned short u16;
typedef float f32;
extern f32 sqrtf(f32);
#pragma intrinsic(sqrtf)
extern void func_801E8AB0_5A4A80(void*,int);
#define P(obj,o) (*(void **)((u8 *)(obj)+(o)))
#define F(obj,o) (*(f32 *)((u8 *)(obj)+(o)))
#define B(obj,o) (*(u8 *)((u8 *)(obj)+(o)))
#define H(obj,o) (*(u16 *)((u8 *)(obj)+(o)))
void func_801E7DF0_5A3DC0(void *arg0) {
volatile unsigned int goemon_negative_control = 1;

 void *ctx;
 f32 vx,vy,vz;
 func_801E8AB0_5A4A80(arg0, 15);
 B(P(arg0,0x5C),0x2C)=0;
 H(P(arg0,0x5C),0x0)=1;
 vz=F(arg0,0x70);vx=F(arg0,0x68);vy=F(arg0,0x6C);
 F(P(arg0,0x5C),0x4)=sqrtf((vz*vz)+((vx*vx)+(vy*vy)))/2;
 F(arg0,0xE4)=F(P(arg0,0x5C),0x4);
 F(arg0,0x70)=0.0f;
 F(arg0,0x6C)=0.0f;
 F(arg0,0x68)=0.0f;
 F(arg0,0xE8)=1.0f;
 H(P(arg0,0x5C),0x2)=H(P(arg0,0x5C),0x1A)|0x400;
}
