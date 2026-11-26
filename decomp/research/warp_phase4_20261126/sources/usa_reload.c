typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef union {u32 word; signed char b[4];} ExitWord;
typedef struct {u8 pad[0xd8]; ExitWord exit;} Task;
typedef struct {u8 pad[0x7898];u8 kind;} Partial;
typedef struct {u8 pad[0x22];u16 flags;} Player;
extern u8 *D_8015C5C8_15D1C8;
extern u8 D_3AE29[],D_CF894[];
extern void *D_801FC60C_5B851C;
extern Player *D_801FC600_5B8510;
extern int func_802154FC_5D09CC(void *,void *,u8);
extern void func_801FB270_5B7180(void),func_80215330_5D0800(Task *),func_802154F0_5D09C0(void),func_8003521C_35E1C(void (*)(void));
void func_80215230_5D0700(Task *task,void *obj) {
    u8 *system=D_8015C5C8_15D1C8;
    Partial *p=(Partial *)(system+0xc8000);
    u32 w;
    if(p->kind && !*(u8 *)(system+(u32)D_3AE29)) {
        w=task->exit.word;
        if(p->kind>=17) {
            if(D_801FC60C_5B851C && func_802154FC_5D09CC(D_801FC60C_5B851C,obj,((signed char *)&w)[2]&0xf0)==0x7fff) {
                D_801FC600_5B8510->flags |= 4;
                func_801FB270_5B7180();
                system=D_8015C5C8_15D1C8;
                *(void **)(system+(u32)D_CF894)=D_801FC60C_5B851C;
                func_80215330_5D0800(task);
                func_8003521C_35E1C(func_802154F0_5D09C0);
            }
        } else if((((signed char *)&w)[2]&0xf)==p->kind) {
            func_80215330_5D0800(task);
            func_8003521C_35E1C(func_802154F0_5D09C0);
        }
    }
}
