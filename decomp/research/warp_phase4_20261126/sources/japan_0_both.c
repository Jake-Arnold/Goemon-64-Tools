typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef union {u32 word; signed char b[4];} ExitWord;
typedef struct {u8 pad[0xd8]; ExitWord exit;} Task;
typedef struct {u8 pad[0x7898];u8 kind;} Partial;
typedef struct {u8 pad[0x22];u16 flags;} Player;
extern u8 *g_system_ptr;
extern u8 D_3AE29[],D_CF894[];
extern void *D_8020151C_5BD4EC;
extern Player *D_80201510_5BD4E0;
extern int func_8021A28C_5D581C(void *,void *,u8);
extern void func_80200180_5BC150(void),func_8021A0C0_5D5650(Task *),func_8021A280_5D5810(void),func_80034E8C_35A8C(void (*)(void));
void func_80219FC0_5D5550(Task *task,void *obj) {
    u8 *system=g_system_ptr;
    Partial *p=(Partial *)(system+0xc8000);
    u32 w;
    if(p->kind && !*(u8 *)(system+(u32)D_3AE29)) {
        w=task->exit.word;
        if(p->kind>=17) {
            if(D_8020151C_5BD4EC && func_8021A28C_5D581C(D_8020151C_5BD4EC,obj,((signed char *)&w)[2]&0xf0)==0x7fff) {
                D_80201510_5BD4E0->flags |= 4;
                func_80200180_5BC150();
                *(void **)(g_system_ptr+(u32)D_CF894)=D_8020151C_5BD4EC; func_8021A0C0_5D5650(task);
                func_80034E8C_35A8C(func_8021A280_5D5810);
            }
        } else if(p->kind==(((signed char *)&w)[2]&0xf)) {
            func_8021A0C0_5D5650(task);
            func_80034E8C_35A8C(func_8021A280_5D5810);
        }
    }
}
