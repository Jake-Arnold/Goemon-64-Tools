/* Research-only Ghost Toys overlay entrance; not integrated or matching C. */
typedef signed int s32; typedef unsigned int u32;typedef unsigned char u8;
typedef struct { u8 unknown[0x60]; u32 flags; } Task;
#ifndef GHOST_HOST
extern u8 func_800240DC_24CDC[];
extern u8 func_80024038_24C38[];
extern u8 func_80038B98_39798[];
extern u8 func_8003521C_35E1C[];
extern void func_0800651C_6F99FC(Task *,void *);
#define TEST_FLAG ((s32 (*)(s32))func_800240DC_24CDC)
#define SET_FLAG ((void (*)(s32))func_80024038_24C38)
#define RUN_HELPER ((void (*)(s32))func_80038B98_39798)
#define SET_CALLBACK ((void (*)(void (*)(Task *,void *)))func_8003521C_35E1C)
#else
extern s32 TEST_FLAG(s32);
extern void SET_FLAG(s32);
extern void RUN_HELPER(s32);
extern void SET_CALLBACK(void (*)(Task *,void *));
extern void func_0800651C_6F99FC(Task *,void *);
#endif
void func_08006490_6F9970(Task *task, void *unused) {
  s32 (*test)(s32) = TEST_FLAG;
  (void)unused;
  if (test(0x19A) && test(0x19B)) {
    SET_FLAG(0x19C);
    task->flags |= 1u;
    RUN_HELPER(0x224);
    SET_CALLBACK(func_0800651C_6F99FC);
  }
}
