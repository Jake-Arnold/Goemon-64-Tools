typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern char func_80223E9C_5DF36C;
extern void* D_801FC604_5B8514;
struct Actor {char pad[0x70];void* ptr;u8 mode;};
void func_08000C64_733B94(struct Actor *actor, void *arg1) {
 actor->mode=0;
 actor->ptr=((void*(*)(void*,void*,void*))&func_80223E9C_5DF36C)(D_801FC604_5B8514,arg1,&actor->mode);
}
