typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern char func_80228C0C_5E419C;
extern void* D_80201514_5BD4E4;
struct Actor {char pad[0x70];void* ptr;u8 mode;};
void func_08000C64_737F44(struct Actor *actor, void *arg1) {
 actor->mode=0;
 actor->ptr=((void*(*)(void*,void*,void*))&func_80228C0C_5E419C)(D_80201514_5BD4E4,arg1,&actor->mode);
}
